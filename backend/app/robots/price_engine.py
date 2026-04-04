from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ChannelListing, PriceHistory, ProductCandidate
from app.robots.common import log_activity


def run(db: Session) -> dict:
    listings = db.scalars(select(ChannelListing)).all()
    changes = 0
    for listing in listings:
        product = db.get(ProductCandidate, listing.product_id)
        if not product:
            continue
        old_price = product.sell_price
        new_price = round(max(product.unit_cost * 1.25, product.sell_price * 0.98), 2)
        if new_price == old_price:
            continue
        product.sell_price = new_price
        db.add(
            PriceHistory(
                product_id=product.id,
                channel=listing.channel,
                old_price=old_price,
                new_price=new_price,
                reason="value_position",
            )
        )
        changes += 1
    db.commit()
    log_activity(db, "Price Engine", f"Processed competitor repricing on {changes} listings.")
    return {"changes": changes}

