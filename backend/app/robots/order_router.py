from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ExceptionRecord, Order, OrderMapping, ProductCandidate
from app.robots.common import log_activity


def run(db: Session) -> dict:
    orders = db.scalars(select(Order).order_by(Order.created_at.desc()).limit(5)).all()
    routed = 0
    for order in orders:
        exists = db.scalar(select(OrderMapping.id).where(OrderMapping.our_order_id == order.id))
        if exists:
            continue
        product = db.get(ProductCandidate, order.product_id)
        if not product:
            db.add(
                ExceptionRecord(
                    type="routing_error",
                    description=f"Product missing for order {order.id}",
                    order_id=order.id,
                    severity="high",
                )
            )
            continue
        db.add(
            OrderMapping(
                our_order_id=order.id,
                supplier_order_id=f"{product.supplier_id}-order-{order.id}",
                supplier_name=product.supplier_name,
                tracking_number=f"TRK{order.id:06d}",
                status="tracking_pending",
            )
        )
        routed += 1
    db.commit()
    log_activity(db, "Order Router", f"Routed {routed} incoming orders to supplier APIs.")
    return {"routed": routed}

