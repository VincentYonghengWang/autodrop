from __future__ import annotations

from datetime import datetime, timedelta
from random import randint, uniform

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    ChannelListing,
    ExceptionRecord,
    InfluencerPost,
    Order,
    PriceHistory,
    ProductCandidate,
    RobotActivity,
    TrendSignal,
)


def seed_demo_data(db: Session) -> None:
    existing = db.scalar(select(TrendSignal.id).limit(1))
    if existing:
        return

    signals = [
        TrendSignal(
            source="tiktok",
            product_name="Portable Ice Plunge Tub",
            viral_score=88,
            raw_url="https://www.tiktok.com/@nova/video/1",
        ),
        TrendSignal(
            source="instagram",
            product_name="Rechargeable Neck Fan",
            viral_score=76,
            raw_url="https://www.instagram.com/reel/2",
        ),
        TrendSignal(
            source="douyin",
            product_name="LED Jellyfish Desk Lamp",
            viral_score=81,
            factory_hint_json={"city": "深圳", "category": "electronics", "factory_count": 140},
            raw_url="https://www.douyin.com/video/3",
        ),
        TrendSignal(
            source="amazon",
            product_name="Pet Hair Remover Roller",
            viral_score=67,
            raw_url="https://www.amazon.com/dp/demo",
        ),
    ]
    db.add_all(signals)
    db.flush()

    products = [
        ProductCandidate(
            product_name="Portable Ice Plunge Tub",
            supplier_id="cj-1001",
            supplier_name="CJ Dropshipping",
            unit_cost=42.0,
            sell_price=129.0,
            margin=0.31,
            status="winner",
            channels_json=["shopify", "tiktok_shop", "instagram"],
            assets_json={"hero": "Generated lifestyle creative ready"},
        ),
        ProductCandidate(
            product_name="Rechargeable Neck Fan",
            supplier_id="sp-2302",
            supplier_name="Spocket",
            unit_cost=11.0,
            sell_price=34.0,
            margin=0.24,
            status="testing",
            channels_json=["shopify", "amazon", "instagram"],
            assets_json={"hero": "Aesthetic summer reel queued"},
        ),
        ProductCandidate(
            product_name="LED Jellyfish Desk Lamp",
            supplier_id="1688-sz-5",
            supplier_name="Shenzhen Factory Cluster",
            unit_cost=8.5,
            sell_price=29.0,
            margin=0.27,
            status="publishing",
            factory_hint_json={"city": "深圳", "category": "electronics", "factory_count": 140},
            channels_json=["shopify", "tiktok_shop", "youtube"],
            assets_json={"hero": "AI influencer video rendering"},
        ),
    ]
    db.add_all(products)
    db.flush()

    listings = [
        ChannelListing(product_id=products[0].id, channel="shopify", listing_id="shp-1", listing_url="https://store/p/ice-plunge"),
        ChannelListing(product_id=products[0].id, channel="tiktok_shop", listing_id="tt-1", listing_url="https://tiktok.com/shop/ice-plunge"),
        ChannelListing(product_id=products[1].id, channel="amazon", listing_id="amz-2", listing_url="https://amazon.com/dp/neckfan"),
        ChannelListing(product_id=products[2].id, channel="shopify", listing_id="shp-3", listing_url="https://store/p/jellyfish-lamp", status="syncing"),
    ]
    db.add_all(listings)

    for product in products:
        db.add(
            Order(
                channel_order_id=f"ORD-{product.id}",
                product_id=product.id,
                customer_email=f"buyer{product.id}@example.com",
                revenue=round(product.sell_price * uniform(0.95, 1.05), 2),
                created_at=datetime.utcnow() - timedelta(hours=randint(2, 72)),
            )
        )

    db.add_all(
        [
            InfluencerPost(product_id=products[0].id, persona="Nova", platform="tiktok", views=32144, likes=2388, comments=141, link_clicks=512),
            InfluencerPost(product_id=products[1].id, persona="Lux", platform="instagram", views=18903, likes=1174, comments=88, link_clicks=274),
            InfluencerPost(product_id=products[2].id, persona="Vida", platform="youtube", views=9942, likes=649, comments=34, link_clicks=193),
            PriceHistory(product_id=products[1].id, channel="amazon", old_price=36.0, new_price=34.0, reason="beat_by_5pct"),
            ExceptionRecord(type="supplier_oos", description="Neck Fan variant Blue is out of stock at Zendrop fallback.", order_id=2, severity="high"),
            ExceptionRecord(type="refund_review", description="Refund request for order #1 exceeds auto-approve threshold.", order_id=1, severity="medium"),
        ]
    )

    db.add_all(
        [
            RobotActivity(robot_name="Trend Radar", message="4 new cross-platform signals scored above threshold.", status="success"),
            RobotActivity(robot_name="Product Scout", message="Shenzhen factory hint attached to Jellyfish Lamp shortlist.", status="success"),
            RobotActivity(robot_name="Influencer Factory", message="Nova TikTok concept rendered and queued for publishing.", status="running"),
            RobotActivity(robot_name="Order Router", message="Fallback supplier requested for Neck Fan blue variant.", status="warning"),
            RobotActivity(robot_name="Analytics Brain", message="Portable Ice Plunge Tub promoted to winner cohort.", status="success"),
        ]
    )

    db.commit()

