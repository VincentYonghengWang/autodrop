from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ExceptionRecord, Order, ProductCandidate, RobotActivity, TrendSignal
from app.schemas import ActivityItem, DashboardResponse, ExceptionItem, MetricCard, PipelineStage, ProductRow


def get_dashboard_payload(db: Session) -> DashboardResponse:
    revenue = db.scalar(select(func.coalesce(func.sum(Order.revenue), 0.0))) or 0.0
    product_count = db.scalar(select(func.count(ProductCandidate.id))) or 0
    trend_count = db.scalar(select(func.count(TrendSignal.id))) or 0
    open_exceptions = db.scalar(select(func.count(ExceptionRecord.id)).where(ExceptionRecord.status == "open")) or 0

    metrics = [
        MetricCard(title="24h Revenue", value=f"${revenue:,.0f}", delta="+18.2%", tone="good"),
        MetricCard(title="Live Tests", value=str(product_count), delta=f"{trend_count} signals", tone="neutral"),
        MetricCard(title="Open Exceptions", value=str(open_exceptions), delta="Needs review", tone="warn"),
        MetricCard(title="Winner Rate", value="12.4%", delta="+2.1 pts", tone="good"),
    ]

    pipeline = [
        PipelineStage(name="Trend Radar", count=trend_count, detail="Scored signals across TikTok, Instagram, Douyin, Amazon, Google"),
        PipelineStage(name="Product Scout", count=product_count, detail="Supplier, margin, and compliance screening"),
        PipelineStage(name="Listing Factory", count=db.scalar(select(func.count(ProductCandidate.id)).where(ProductCandidate.status == "publishing")) or 0, detail="Assets and channel copy in production"),
        PipelineStage(name="Publish + Route", count=db.scalar(select(func.count(Order.id))) or 0, detail="Listings, orders, and supplier routing"),
        PipelineStage(name="Analytics Brain", count=db.scalar(select(func.count(ProductCandidate.id)).where(ProductCandidate.status == "winner")) or 0, detail="Winners promoted, losers killed, budgets updated"),
    ]

    products = []
    for product in db.scalars(select(ProductCandidate).order_by(ProductCandidate.created_at.desc()).limit(10)).all():
        signal = db.scalar(select(TrendSignal).where(TrendSignal.product_name == product.product_name).limit(1))
        products.append(
            ProductRow(
                id=product.id,
                product_name=product.product_name,
                source=signal.source if signal else "system",
                margin=product.margin,
                status=product.status,
                channels=product.channels_json,
                factory_hint=product.factory_hint_json,
                created_at=product.created_at,
            )
        )

    activity = [
        ActivityItem(
            robot_name=item.robot_name,
            message=item.message,
            status=item.status,
            created_at=item.created_at,
        )
        for item in db.scalars(select(RobotActivity).order_by(RobotActivity.created_at.desc()).limit(8)).all()
    ]

    exceptions = [
        ExceptionItem(
            id=item.id,
            type=item.type,
            description=item.description,
            status=item.status,
            severity=item.severity,
            created_at=item.created_at,
        )
        for item in db.scalars(select(ExceptionRecord).order_by(ExceptionRecord.created_at.desc()).limit(8)).all()
    ]

    return DashboardResponse(
        metrics=metrics,
        pipeline=pipeline,
        products=products,
        activity=activity,
        exceptions=exceptions,
    )

