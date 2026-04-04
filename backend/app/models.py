from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class TrendSignal(Base):
    __tablename__ = "trend_signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(50), index=True)
    product_name: Mapped[str] = mapped_column(String(255), index=True)
    viral_score: Mapped[float] = mapped_column(Float)
    factory_hint_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    raw_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class ProductCandidate(Base):
    __tablename__ = "product_candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(255), index=True)
    supplier_id: Mapped[str] = mapped_column(String(100))
    supplier_name: Mapped[str] = mapped_column(String(100))
    unit_cost: Mapped[float] = mapped_column(Float)
    sell_price: Mapped[float] = mapped_column(Float)
    margin: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="approved", index=True)
    factory_hint_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    channels_json: Mapped[list[str]] = mapped_column(JSON, default=list)
    assets_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    listings: Mapped[list[ChannelListing]] = relationship(back_populates="product")


class RejectedProduct(Base):
    __tablename__ = "rejected_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(255), index=True)
    reason: Mapped[str] = mapped_column(Text)
    source_signal_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ChannelListing(Base):
    __tablename__ = "channel_listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product_candidates.id"), index=True)
    channel: Mapped[str] = mapped_column(String(50), index=True)
    listing_id: Mapped[str] = mapped_column(String(100))
    listing_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="published")
    published_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product: Mapped[ProductCandidate] = relationship(back_populates="listings")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel_order_id: Mapped[str] = mapped_column(String(100), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product_candidates.id"), index=True)
    customer_email: Mapped[str] = mapped_column(String(255), index=True)
    revenue: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="paid")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class OrderMapping(Base):
    __tablename__ = "order_mappings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    our_order_id: Mapped[int] = mapped_column(Integer, index=True)
    supplier_order_id: Mapped[str] = mapped_column(String(100), index=True)
    supplier_name: Mapped[str] = mapped_column(String(100))
    tracking_number: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ordered")


class InfluencerPost(Base):
    __tablename__ = "influencer_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product_candidates.id"), index=True)
    persona: Mapped[str] = mapped_column(String(100))
    platform: Mapped[str] = mapped_column(String(50), index=True)
    post_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    views: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)
    link_clicks: Mapped[int] = mapped_column(Integer, default=0)
    posted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product_candidates.id"), index=True)
    channel: Mapped[str] = mapped_column(String(50))
    old_price: Mapped[float] = mapped_column(Float)
    new_price: Mapped[float] = mapped_column(Float)
    reason: Mapped[str] = mapped_column(String(255))
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ExceptionRecord(Base):
    __tablename__ = "exceptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str] = mapped_column(Text)
    order_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="open")
    severity: Mapped[str] = mapped_column(String(50), default="medium")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RobotActivity(Base):
    __tablename__ = "robot_activity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    robot_name: Mapped[str] = mapped_column(String(80), index=True)
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="success")
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

