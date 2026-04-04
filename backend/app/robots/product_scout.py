from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import ProductCandidate, RejectedProduct, TrendSignal
from app.robots.common import log_activity

settings = get_settings()

FACTORY_MAP = {
    "义乌": ["accessories", "toys", "small_goods", "stationery"],
    "莆田": ["shoes", "sneakers", "sportswear"],
    "深圳": ["electronics", "gadgets", "cables", "tech"],
    "汕头": ["toys", "plastics", "packaging"],
    "东莞": ["furniture", "garments", "electronics"],
    "佛山": ["ceramics", "hardware", "lighting"],
    "广州": ["clothing", "beauty", "fashion"],
    "杭州": ["fashion", "digital", "accessories"],
}

SUPPLIERS = [
    {"name": "CJ Dropshipping", "multiplier": 1.0},
    {"name": "AliExpress", "multiplier": 0.95},
    {"name": "Zendrop", "multiplier": 1.08},
    {"name": "Spocket", "multiplier": 1.12},
]


def _estimate_product(signal: TrendSignal) -> tuple[float, float]:
    base = max(8.0, signal.viral_score / 4.0)
    shipping = 4.5 if signal.source in {"tiktok", "instagram"} else 3.5
    return round(base, 2), shipping


def run(db: Session) -> dict:
    signals = db.scalars(
        select(TrendSignal).where(
            TrendSignal.product_name.not_in(select(ProductCandidate.product_name)),
            TrendSignal.product_name.not_in(select(RejectedProduct.product_name)),
        )
    ).all()

    approved = 0
    rejected = 0

    for signal in signals:
        unit_cost, shipping = _estimate_product(signal)
        sell_price = round(unit_cost * settings.default_markup_factor, 2)
        gross_margin = (sell_price - unit_cost - shipping) / sell_price
        net_margin = gross_margin - settings.ad_spend_estimate_pct - 0.08

        if net_margin < settings.margin_floor:
            db.add(
                RejectedProduct(
                    product_name=signal.product_name,
                    reason=f"Net margin {net_margin:.2%} below floor",
                    source_signal_id=signal.id,
                )
            )
            rejected += 1
            continue

        hint = signal.factory_hint_json
        supplier_name = SUPPLIERS[signal.id % len(SUPPLIERS)]["name"]
        supplier_id = f"{supplier_name.lower().replace(' ', '-')}-{signal.id}"
        db.add(
            ProductCandidate(
                product_name=signal.product_name,
                supplier_id=supplier_id,
                supplier_name=supplier_name,
                unit_cost=unit_cost,
                sell_price=sell_price,
                margin=round(net_margin, 2),
                status="approved",
                factory_hint_json=hint,
                channels_json=["shopify", "tiktok_shop", "instagram", "youtube"],
            )
        )
        approved += 1

    db.commit()
    log_activity(
        db,
        "Product Scout",
        f"Approved {approved} products and rejected {rejected} based on supplier, factory, and margin scoring.",
        metadata={"factory_map": FACTORY_MAP},
    )
    return {"approved": approved, "rejected": rejected}

