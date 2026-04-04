from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Order, OrderMapping, ProductCandidate
from app.robots import analytics_brain, channel_publisher, cs_bot, douyin_intel, influencer_factory, listing_factory, order_router, price_engine, product_scout, trend_radar


def run_sync_task(task_name: str, db: Session) -> dict:
    if task_name == "trend_radar":
        result = trend_radar.run(db)
        product_scout.run(db)
        return result
    if task_name == "douyin_intel":
        result = douyin_intel.run(db)
        product_scout.run(db)
        return result
    if task_name == "listing_pipeline":
        listing_factory.run(db)
        influencer_factory.run(db)
        return channel_publisher.run(db)
    if task_name == "price_engine":
        return price_engine.run(db)
    if task_name == "analytics_brain":
        return analytics_brain.run(db)
    if task_name == "ops_loop":
        order_router.run(db)
        return cs_bot.run(db)
    if task_name == "demo_run_all":
        trend_radar.run(db)
        product_scout.run(db)
        listing_factory.run(db)
        influencer_factory.run(db)
        channel_publisher.run(db)
        price_engine.run(db)
        return analytics_brain.run(db)
    raise ValueError(f"Unsupported task: {task_name}")


def simulate_checkout(db: Session, product_id: int, email: str) -> dict:
    product = db.get(ProductCandidate, product_id)
    if not product:
        raise ValueError("Product not found")

    order = Order(
        channel_order_id=f"web-{product_id}-{email.split('@')[0]}",
        product_id=product.id,
        customer_email=email,
        revenue=product.sell_price,
        status="paid",
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    order_router.run(db)
    analytics_brain.run(db)

    mapping = db.scalar(select(OrderMapping).where(OrderMapping.our_order_id == order.id).limit(1))
    return {
        "order_id": order.id,
        "product_name": product.product_name,
        "revenue": order.revenue,
        "supplier": product.supplier_name,
        "tracking_number": mapping.tracking_number if mapping else None,
        "status": "confirmed",
    }
