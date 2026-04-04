from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Order, ProductCandidate
from app.robots.common import log_activity

settings = get_settings()


def run(db: Session) -> dict:
    winners = 0
    losers = 0
    products = db.scalars(select(ProductCandidate)).all()
    for product in products:
        order_count = db.scalar(select(func.count(Order.id)).where(Order.product_id == product.id)) or 0
        revenue = db.scalar(select(func.coalesce(func.sum(Order.revenue), 0.0)).where(Order.product_id == product.id)) or 0.0
        if order_count >= settings.min_orders_for_winner or revenue >= settings.min_revenue_for_winner:
            product.status = "winner"
            winners += 1
        elif product.status == "live":
            product.status = "killed"
            losers += 1
    db.commit()
    log_activity(db, "Analytics Brain", f"Promoted {winners} winners and killed {losers} underperformers.")
    return {"winners": winners, "losers": losers}

