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


TREND_SIGNALS = [
    {
        "source": "tiktok",
        "product_name": "Portable Ice Plunge Tub",
        "viral_score": 88,
        "raw_url": "https://www.tiktok.com/@nova/video/1",
    },
    {
        "source": "instagram",
        "product_name": "Rechargeable Neck Fan",
        "viral_score": 76,
        "raw_url": "https://www.instagram.com/reel/2",
    },
    {
        "source": "douyin",
        "product_name": "LED Jellyfish Desk Lamp",
        "viral_score": 81,
        "factory_hint_json": {"city": "深圳", "category": "electronics", "factory_count": 140},
        "raw_url": "https://www.douyin.com/video/3",
    },
    {
        "source": "amazon",
        "product_name": "Pet Hair Remover Roller",
        "viral_score": 67,
        "raw_url": "https://www.amazon.com/dp/demo",
    },
    {
        "source": "tiktok",
        "product_name": "Foldable Walking Pad",
        "viral_score": 73,
        "raw_url": "https://www.tiktok.com/@vida/video/5",
    },
    {
        "source": "instagram",
        "product_name": "Magnetic Cable Organizer",
        "viral_score": 69,
        "raw_url": "https://www.instagram.com/reel/6",
    },
    {
        "source": "tiktok",
        "product_name": "Portable Blender Bottle",
        "viral_score": 74,
        "raw_url": "https://www.tiktok.com/@nova/video/7",
    },
    {
        "source": "amazon",
        "product_name": "Sunset Projection Lamp",
        "viral_score": 71,
        "raw_url": "https://www.amazon.com/dp/sunset-lamp",
    },
    {
        "source": "douyin",
        "product_name": "Breathable Slip-On Recovery Shoes",
        "viral_score": 77,
        "factory_hint_json": {"city": "莆田", "category": "shoes", "factory_count": 260},
        "raw_url": "https://www.douyin.com/video/8",
    },
    {
        "source": "instagram",
        "product_name": "Car Seat Gap Organizer",
        "viral_score": 68,
        "raw_url": "https://www.instagram.com/reel/9",
    },
]


PRODUCT_CATALOG = [
    {
        "product_name": "Portable Ice Plunge Tub",
        "supplier_id": "cj-1001",
        "supplier_name": "CJ Dropshipping",
        "unit_cost": 42.0,
        "sell_price": 129.0,
        "margin": 0.31,
        "status": "winner",
        "channels_json": ["shopify", "tiktok_shop", "instagram"],
        "assets_json": {"hero": "Lifestyle plunge content ready"},
    },
    {
        "product_name": "Rechargeable Neck Fan",
        "supplier_id": "sp-2302",
        "supplier_name": "Spocket",
        "unit_cost": 11.0,
        "sell_price": 34.0,
        "margin": 0.24,
        "status": "testing",
        "channels_json": ["shopify", "amazon", "instagram"],
        "assets_json": {"hero": "Aesthetic summer reel queued"},
    },
    {
        "product_name": "LED Jellyfish Desk Lamp",
        "supplier_id": "1688-sz-5",
        "supplier_name": "Shenzhen Factory Cluster",
        "unit_cost": 8.5,
        "sell_price": 29.0,
        "margin": 0.27,
        "status": "publishing",
        "factory_hint_json": {"city": "深圳", "category": "electronics", "factory_count": 140},
        "channels_json": ["shopify", "tiktok_shop", "youtube"],
        "assets_json": {"hero": "AI influencer video rendering"},
    },
    {
        "product_name": "Pet Hair Remover Roller",
        "supplier_id": "cj-4021",
        "supplier_name": "CJ Dropshipping",
        "unit_cost": 14.0,
        "sell_price": 50.25,
        "margin": 0.29,
        "status": "live",
        "channels_json": ["shopify", "amazon", "instagram"],
        "assets_json": {"hero": "Pet cleanup content queued"},
    },
    {
        "product_name": "Foldable Walking Pad",
        "supplier_id": "zr-8841",
        "supplier_name": "Zendrop",
        "unit_cost": 119.0,
        "sell_price": 289.0,
        "margin": 0.23,
        "status": "testing",
        "channels_json": ["shopify", "tiktok_shop"],
        "assets_json": {"hero": "Home office cardio creative packaged"},
    },
    {
        "product_name": "Magnetic Cable Organizer",
        "supplier_id": "alx-7832",
        "supplier_name": "AliExpress Fast Ship",
        "unit_cost": 4.2,
        "sell_price": 18.0,
        "margin": 0.26,
        "status": "publishing",
        "channels_json": ["shopify", "amazon", "tiktok_shop"],
        "assets_json": {"hero": "Desk setup micro-content ready"},
    },
    {
        "product_name": "Portable Blender Bottle",
        "supplier_id": "cj-5512",
        "supplier_name": "CJ Dropshipping",
        "unit_cost": 9.8,
        "sell_price": 28.0,
        "margin": 0.25,
        "status": "live",
        "channels_json": ["shopify", "tiktok_shop", "instagram"],
        "assets_json": {"hero": "Gym and commute UGC package ready"},
    },
    {
        "product_name": "Sunset Projection Lamp",
        "supplier_id": "1688-gz-18",
        "supplier_name": "Guangzhou Lighting Hub",
        "unit_cost": 7.1,
        "sell_price": 24.0,
        "margin": 0.28,
        "status": "testing",
        "channels_json": ["shopify", "amazon", "instagram"],
        "assets_json": {"hero": "Bedroom aesthetic reels in review"},
    },
    {
        "product_name": "Breathable Slip-On Recovery Shoes",
        "supplier_id": "pt-7704",
        "supplier_name": "Putian Factory Network",
        "unit_cost": 16.5,
        "sell_price": 49.0,
        "margin": 0.27,
        "status": "live",
        "factory_hint_json": {"city": "莆田", "category": "shoes", "factory_count": 260},
        "channels_json": ["shopify", "tiktok_shop", "amazon"],
        "assets_json": {"hero": "Comfort-first try-on creative approved"},
    },
    {
        "product_name": "Car Seat Gap Organizer",
        "supplier_id": "zr-2208",
        "supplier_name": "Zendrop",
        "unit_cost": 6.4,
        "sell_price": 22.0,
        "margin": 0.24,
        "status": "publishing",
        "channels_json": ["shopify", "amazon"],
        "assets_json": {"hero": "Auto accessory launch assets bundled"},
    },
]


LISTINGS = {
    "Portable Ice Plunge Tub": [
        ("shopify", "shp-ice-plunge", "https://store/p/ice-plunge", "published"),
        ("tiktok_shop", "tt-ice-plunge", "https://tiktok.com/shop/ice-plunge", "published"),
    ],
    "Rechargeable Neck Fan": [
        ("amazon", "amz-neck-fan", "https://amazon.com/dp/neckfan", "published"),
        ("instagram", "ig-neck-fan", "https://instagram.com/p/neckfan", "published"),
    ],
    "LED Jellyfish Desk Lamp": [
        ("shopify", "shp-jellyfish-lamp", "https://store/p/jellyfish-lamp", "syncing"),
    ],
    "Pet Hair Remover Roller": [
        ("shopify", "shp-pet-roller", "https://store/p/pet-hair-remover", "published"),
        ("amazon", "amz-pet-roller", "https://amazon.com/dp/pethairroller", "published"),
    ],
    "Foldable Walking Pad": [
        ("shopify", "shp-walking-pad", "https://store/p/walking-pad", "published"),
    ],
    "Magnetic Cable Organizer": [
        ("shopify", "shp-cable-organizer", "https://store/p/cable-organizer", "syncing"),
    ],
    "Portable Blender Bottle": [
        ("shopify", "shp-blender-bottle", "https://store/p/blender-bottle", "published"),
        ("tiktok_shop", "tt-blender-bottle", "https://tiktok.com/shop/blender-bottle", "published"),
    ],
    "Sunset Projection Lamp": [
        ("shopify", "shp-sunset-lamp", "https://store/p/sunset-lamp", "published"),
    ],
    "Breathable Slip-On Recovery Shoes": [
        ("shopify", "shp-recovery-shoes", "https://store/p/recovery-shoes", "published"),
        ("amazon", "amz-recovery-shoes", "https://amazon.com/dp/recovery-shoes", "published"),
    ],
    "Car Seat Gap Organizer": [
        ("shopify", "shp-car-gap-organizer", "https://store/p/car-gap-organizer", "syncing"),
    ],
}


INFLUENCER_POSTS = [
    ("Portable Ice Plunge Tub", "Nova", "tiktok", 32144, 2388, 141, 512),
    ("Rechargeable Neck Fan", "Lux", "instagram", 18903, 1174, 88, 274),
    ("LED Jellyfish Desk Lamp", "Vida", "youtube", 9942, 649, 34, 193),
    ("Pet Hair Remover Roller", "Mika", "instagram", 14220, 966, 44, 231),
    ("Foldable Walking Pad", "Nova", "tiktok", 22411, 1532, 97, 341),
    ("Magnetic Cable Organizer", "Lux", "instagram", 11880, 701, 39, 188),
    ("Portable Blender Bottle", "Vida", "youtube", 16420, 911, 58, 226),
    ("Sunset Projection Lamp", "Lux", "instagram", 21502, 1430, 85, 319),
    ("Breathable Slip-On Recovery Shoes", "Nova", "tiktok", 28774, 1938, 122, 407),
    ("Car Seat Gap Organizer", "Vida", "youtube", 9080, 522, 29, 141),
]


PRICE_EVENTS = [
    ("Rechargeable Neck Fan", "amazon", 36.0, 34.0, "beat_by_5pct"),
    ("Magnetic Cable Organizer", "shopify", 19.5, 18.0, "match_lowest"),
    ("Portable Blender Bottle", "shopify", 30.0, 28.0, "value_position"),
    ("Sunset Projection Lamp", "amazon", 26.0, 24.0, "beat_by_5pct"),
]


EXCEPTIONS = [
    ("supplier_oos", "Neck Fan variant Blue is out of stock at Zendrop fallback.", 2, "high"),
    ("refund_review", "Refund request for order #1 exceeds auto-approve threshold.", 1, "medium"),
]


ROBOT_UPDATES = [
    ("Trend Radar", "6 cross-platform signals scored above threshold.", "success"),
    ("Product Scout", "Three new products cleared supplier and margin filters.", "success"),
    ("Influencer Factory", "Launch creatives rendered for Walking Pad and Cable Organizer.", "running"),
    ("Order Router", "Fallback supplier requested for Neck Fan blue variant.", "warning"),
    ("Analytics Brain", "Portable Ice Plunge Tub remains in winner cohort.", "success"),
]


def _get_product_by_name(db: Session, product_name: str) -> ProductCandidate | None:
    return db.scalar(select(ProductCandidate).where(ProductCandidate.product_name == product_name).limit(1))


def _get_signal_by_name(db: Session, product_name: str) -> TrendSignal | None:
    return db.scalar(select(TrendSignal).where(TrendSignal.product_name == product_name).limit(1))


def seed_demo_data(db: Session) -> None:
    for signal_payload in TREND_SIGNALS:
        if _get_signal_by_name(db, signal_payload["product_name"]):
            continue
        db.add(TrendSignal(**signal_payload))

    db.flush()

    product_map: dict[str, ProductCandidate] = {}
    for product_payload in PRODUCT_CATALOG:
        product = _get_product_by_name(db, product_payload["product_name"])
        if product is None:
            product = ProductCandidate(**product_payload)
            db.add(product)
            db.flush()
        product_map[product.product_name] = product

    for product_name, listing_rows in LISTINGS.items():
        product = product_map[product_name]
        for channel, listing_id, listing_url, status in listing_rows:
            existing_listing = db.scalar(
                select(ChannelListing)
                .where(ChannelListing.product_id == product.id, ChannelListing.channel == channel)
                .limit(1)
            )
            if existing_listing:
                continue
            db.add(
                ChannelListing(
                    product_id=product.id,
                    channel=channel,
                    listing_id=listing_id,
                    listing_url=listing_url,
                    status=status,
                )
            )

    for product_name, persona, platform, views, likes, comments, link_clicks in INFLUENCER_POSTS:
        product = product_map[product_name]
        existing_post = db.scalar(
            select(InfluencerPost)
            .where(
                InfluencerPost.product_id == product.id,
                InfluencerPost.persona == persona,
                InfluencerPost.platform == platform,
            )
            .limit(1)
        )
        if existing_post:
            continue
        db.add(
            InfluencerPost(
                product_id=product.id,
                persona=persona,
                platform=platform,
                views=views,
                likes=likes,
                comments=comments,
                link_clicks=link_clicks,
            )
        )

    for product_name, channel, old_price, new_price, reason in PRICE_EVENTS:
        product = product_map[product_name]
        existing_change = db.scalar(
            select(PriceHistory)
            .where(PriceHistory.product_id == product.id, PriceHistory.channel == channel, PriceHistory.reason == reason)
            .limit(1)
        )
        if existing_change:
            continue
        db.add(
            PriceHistory(
                product_id=product.id,
                channel=channel,
                old_price=old_price,
                new_price=new_price,
                reason=reason,
            )
        )

    existing_exception_count = db.scalar(select(ExceptionRecord.id).limit(1))
    if not existing_exception_count:
        for exception_type, description, order_id, severity in EXCEPTIONS:
            db.add(
                ExceptionRecord(
                    type=exception_type,
                    description=description,
                    order_id=order_id,
                    severity=severity,
                )
            )

    for product in product_map.values():
        existing_order = db.scalar(select(Order.id).where(Order.product_id == product.id).limit(1))
        if existing_order:
            continue
        db.add(
            Order(
                channel_order_id=f"ORD-{product.id}",
                product_id=product.id,
                customer_email=f"buyer{product.id}@example.com",
                revenue=round(product.sell_price * uniform(0.95, 1.05), 2),
                created_at=datetime.utcnow() - timedelta(hours=randint(2, 72)),
            )
        )

    for robot_name, message, status in ROBOT_UPDATES:
        existing_activity = db.scalar(
            select(RobotActivity.id).where(RobotActivity.robot_name == robot_name, RobotActivity.message == message).limit(1)
        )
        if existing_activity:
            continue
        db.add(RobotActivity(robot_name=robot_name, message=message, status=status))

    db.commit()
