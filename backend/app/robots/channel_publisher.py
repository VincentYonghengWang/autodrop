from __future__ import annotations

import asyncio

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ChannelListing, ProductCandidate
from app.robots.common import log_activity


async def publish_channel(product: ProductCandidate, channel: str) -> dict:
    await asyncio.sleep(0)
    return {
        "product_id": product.id,
        "channel": channel,
        "listing_id": f"{channel[:3]}-{product.id}",
        "listing_url": f"https://{channel}.autodrop.local/products/{product.id}",
    }


async def publish_all(product: ProductCandidate) -> list[dict]:
    return await asyncio.gather(*(publish_channel(product, channel) for channel in product.channels_json))


def run(db: Session) -> dict:
    products = db.scalars(select(ProductCandidate).where(ProductCandidate.status == "publishing")).all()
    payloads: list[dict] = []
    for product in products:
        results = asyncio.run(publish_all(product))
        for result in results:
            payloads.append(result)
            db.add(
                ChannelListing(
                    product_id=result["product_id"],
                    channel=result["channel"],
                    listing_id=result["listing_id"],
                    listing_url=result["listing_url"],
                    status="published",
                )
            )
        product.status = "live"
    db.commit()
    log_activity(db, "Multi-Channel Publisher", f"Published {len(payloads)} listings in parallel across sales and content channels.")
    return {"published": len(payloads)}
