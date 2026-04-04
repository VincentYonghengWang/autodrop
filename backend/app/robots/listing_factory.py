from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ProductCandidate
from app.robots.common import log_activity


def run(db: Session) -> dict:
    products = db.scalars(select(ProductCandidate).where(ProductCandidate.status == "approved")).all()
    updated = 0
    for product in products:
        product.assets_json = {
            "shopify": {
                "title": product.product_name,
                "description_html": f"<p>{product.product_name} optimized for high-converting storefronts.</p>",
            },
            "tiktok": {
                "title": f"{product.product_name} | Viral Pick",
                "hashtags": ["#autodrop", "#viralfinds"],
            },
            "instagram": {
                "captions": [
                    f"Quiet luxury energy, practical payoff. {product.product_name}.",
                    f"Daily-use upgrade: {product.product_name}.",
                ]
            },
        }
        product.status = "publishing"
        updated += 1
    db.commit()
    log_activity(db, "Listing Factory", f"Generated channel copy and media briefs for {updated} products.")
    return {"updated": updated}

