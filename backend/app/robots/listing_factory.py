from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ProductCandidate
from app.robots.common import log_activity
from app.services.minimax import generate_product_copy


def run(db: Session) -> dict:
    products = db.scalars(select(ProductCandidate).where(ProductCandidate.status == "approved")).all()
    updated = 0
    for product in products:
        ai_copy = generate_product_copy(
            product_name=product.product_name,
            source=(product.channels_json[0] if product.channels_json else None),
            factory_hint=product.factory_hint_json,
        )
        product.assets_json = {
            "shopify": {
                "title": (ai_copy or {}).get("shopify_title", product.product_name),
                "description_html": (ai_copy or {}).get(
                    "shopify_description_html",
                    f"<p>{product.product_name} optimized for high-converting storefronts.</p>",
                ),
            },
            "tiktok": {
                "title": (ai_copy or {}).get("tiktok_title", f"{product.product_name} | Viral Pick"),
                "hashtags": (ai_copy or {}).get("tiktok_hashtags", ["#autodrop", "#viralfinds"]),
            },
            "instagram": {
                "captions": (ai_copy or {}).get(
                    "instagram_captions",
                    [
                        f"Quiet luxury energy, practical payoff. {product.product_name}.",
                        f"Daily-use upgrade: {product.product_name}.",
                    ],
                )
            },
        }
        product.status = "publishing"
        updated += 1
    db.commit()
    log_activity(
        db,
        "Listing Factory",
        f"Generated channel copy and media briefs for {updated} products.",
        metadata={"provider": "minimax" if products else "fallback"},
    )
    return {"updated": updated}
