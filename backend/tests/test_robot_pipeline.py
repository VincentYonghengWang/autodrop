from __future__ import annotations

from sqlalchemy import func
from sqlalchemy import select

from app.core.config import get_settings
from app.models import (
    ChannelListing,
    InfluencerPost,
    Order,
    OrderMapping,
    PriceHistory,
    ProductCandidate,
    RobotActivity,
    TrendSignal,
)
from app.robots import analytics_brain, channel_publisher, influencer_factory, listing_factory, order_router, price_engine, product_scout, trend_radar

settings = get_settings()


def test_trend_to_candidate_pipeline(db_session) -> None:
    trend_result = trend_radar.run(db_session)
    scout_result = product_scout.run(db_session)

    trend_count = db_session.scalar(select(func.count(TrendSignal.id)))
    approved_products = db_session.scalars(select(ProductCandidate)).all()

    assert trend_result["inserted"] == 2
    assert scout_result["approved"] == 2
    assert trend_count == 2
    assert len(approved_products) == 2
    assert all(product.status == "approved" for product in approved_products)

    second_run = trend_radar.run(db_session)
    assert second_run["inserted"] == 0
    assert second_run["skipped"] is True


def test_end_to_end_demo_robot_flow(db_session) -> None:
    trend_radar.run(db_session)
    product_scout.run(db_session)
    listing_factory.run(db_session)
    influencer_factory.run(db_session)
    publish_result = channel_publisher.run(db_session)

    products = db_session.scalars(select(ProductCandidate).order_by(ProductCandidate.id)).all()
    assert products
    assert all(product.status == "live" for product in products)
    assert publish_result["published"] == sum(len(product.channels_json) for product in products)

    for product in products:
        for index in range(settings.min_orders_for_winner):
            db_session.add(
                Order(
                    channel_order_id=f"demo-order-{product.id}-{index}",
                    product_id=product.id,
                    customer_email=f"buyer{product.id}-{index}@example.com",
                    revenue=product.sell_price,
                )
            )
    db_session.commit()

    order_result = order_router.run(db_session)
    price_result = price_engine.run(db_session)
    analytics_result = analytics_brain.run(db_session)

    listings = db_session.scalars(select(ChannelListing)).all()
    influencer_posts = db_session.scalars(select(InfluencerPost)).all()
    order_mappings = db_session.scalars(select(OrderMapping)).all()
    price_changes = db_session.scalars(select(PriceHistory)).all()
    activity = db_session.scalars(select(RobotActivity)).all()
    expected_routed = min(5, len(products) * settings.min_orders_for_winner)

    assert listings
    assert len(influencer_posts) == len(products) * 3
    assert order_result["routed"] == expected_routed
    assert len(order_mappings) == expected_routed
    assert price_result["changes"] == len(listings)
    assert len(price_changes) == len(listings)
    assert analytics_result["winners"] == len(products)
    assert any(item.robot_name == "Analytics Brain" for item in activity)
