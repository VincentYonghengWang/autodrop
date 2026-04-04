from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import InfluencerPost, ProductCandidate
from app.robots.common import log_activity

PERSONAS = [
    {"name": "Nova", "platform": "tiktok", "style": "Gen-Z, energetic, beauty-tech"},
    {"name": "Lux", "platform": "instagram", "style": "minimalist, aesthetic, lifestyle"},
    {"name": "Vida", "platform": "youtube", "style": "authentic, budget-friendly, practical"},
]


def run(db: Session) -> dict:
    products = db.scalars(select(ProductCandidate).where(ProductCandidate.status == "publishing")).all()
    created = 0
    for product in products:
        for persona in PERSONAS:
            db.add(
                InfluencerPost(
                    product_id=product.id,
                    persona=persona["name"],
                    platform=persona["platform"],
                    post_url=f"https://content.autodrop.ai/{persona['platform']}/{product.id}",
                    views=0,
                    likes=0,
                    comments=0,
                    link_clicks=0,
                )
            )
            created += 1
    db.commit()
    log_activity(db, "Influencer Factory", f"Queued {created} AI influencer assets across TikTok, Instagram, and YouTube.")
    return {"created": created}

