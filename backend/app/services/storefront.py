from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ProductCandidate, TrendSignal
from app.schemas import StorefrontProduct, StorefrontResponse

IMAGE_TONES = ["peach", "mint", "lavender", "sky"]


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


def get_storefront_payload(db: Session) -> StorefrontResponse:
    products = db.scalars(
        select(ProductCandidate)
        .where(ProductCandidate.status.in_(["winner", "live", "publishing", "testing"]))
        .order_by(ProductCandidate.created_at.desc())
        .limit(8)
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
    return StorefrontResponse(
        products=rows,
        hero_product=hero_product,
        total_products=len(rows),
        updated_label="Updated from live demo data",
    )
