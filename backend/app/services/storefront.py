from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ProductCandidate, TrendSignal
from app.schemas import InfluencerCard, StorefrontProduct, StorefrontResponse
from app.services.minimax import generate_influencer_copy

IMAGE_TONES = ["peach", "mint", "lavender", "sky"]
FALLBACK_INFLUENCER_CARDS = [
    {
        "platform": "TikTok",
        "handle": "@nova.picks",
        "title": "Fast first-impression hook built for scroll-stopping reach",
        "stats": "2.3M views · 187K likes · 4.2K comments",
        "theme": "obsidian",
    },
    {
        "platform": "Instagram",
        "handle": "@lux.styled",
        "title": "Aesthetic lifestyle reel framed around daily use",
        "stats": "1.1M views · 94K likes · 2.1K saves",
        "theme": "forest",
    },
    {
        "platform": "YouTube Shorts",
        "handle": "@vida.finds",
        "title": "Practical review format with a clean conversion CTA",
        "stats": "840K views · 61K likes · 3.8K comments",
        "theme": "mahogany",
    },
]


def _badge_for_status(status: str) -> str:
    return {
        "winner": "Best seller",
        "live": "Live now",
        "publishing": "Launching",
        "testing": "Trending",
        "approved": "Queued",
    }.get(status, "Trending")


def _subtitle_for_product(product: ProductCandidate, signal: TrendSignal | None) -> str:
    parts = []
    if signal:
        parts.append(f"Spotted on {signal.source.title()}")
    if product.factory_hint_json and product.factory_hint_json.get("city"):
        parts.append(f"Sourced via {product.factory_hint_json['city']} factory cluster")
    else:
        parts.append(f"Fulfilled by {product.supplier_name}")
    return " · ".join(parts)


def _get_influencer_cards(product: ProductCandidate, signal: TrendSignal | None, db: Session) -> list[InfluencerCard]:
    assets = dict(product.assets_json or {})
    existing_cards = assets.get("influencer_cards")
    cards_payload = existing_cards if isinstance(existing_cards, list) and existing_cards else None

    if cards_payload is None:
        cards_payload = generate_influencer_copy(
            product_name=product.product_name,
            source=signal.source if signal else None,
            factory_hint=product.factory_hint_json,
        ) or FALLBACK_INFLUENCER_CARDS
        assets["influencer_cards"] = cards_payload
        product.assets_json = assets
        db.commit()
        db.refresh(product)

    return [InfluencerCard(**card) for card in cards_payload[:3]]


def get_storefront_payload(db: Session) -> StorefrontResponse:
    products = db.scalars(
        select(ProductCandidate)
        .where(ProductCandidate.status.in_(["winner", "live", "publishing", "testing"]))
        .order_by(ProductCandidate.created_at.desc())
        .limit(12)
    ).all()

    rows: list[StorefrontProduct] = []
    for index, product in enumerate(products):
        signal = db.scalar(select(TrendSignal).where(TrendSignal.product_name == product.product_name).limit(1))
        rows.append(
            StorefrontProduct(
                id=product.id,
                product_name=product.product_name,
                source=signal.source if signal else "system",
                status=product.status,
                price=round(product.sell_price, 2),
                compare_at_price=round(product.sell_price * 1.5, 2),
                margin=product.margin,
                channels=product.channels_json,
                factory_hint=product.factory_hint_json,
                badge=_badge_for_status(product.status),
                subtitle=_subtitle_for_product(product, signal),
                image_tone=IMAGE_TONES[index % len(IMAGE_TONES)],
            )
        )

    hero_product = rows[0] if rows else None
    hero_source = db.scalar(select(TrendSignal).where(TrendSignal.product_name == hero_product.product_name).limit(1)) if hero_product else None
    hero_model = products[0] if products else None
    return StorefrontResponse(
        products=rows,
        hero_product=hero_product,
        influencer_cards=_get_influencer_cards(hero_model, hero_source, db) if hero_model and hero_product else [],
        total_products=len(rows),
        updated_label="Updated from live automation data",
    )
