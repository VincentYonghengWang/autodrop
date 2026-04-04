from datetime import datetime

from pydantic import BaseModel


class MetricCard(BaseModel):
    title: str
    value: str
    delta: str
    tone: str


class PipelineStage(BaseModel):
    name: str
    count: int
    detail: str


class ProductRow(BaseModel):
    id: int
    product_name: str
    source: str
    margin: float
    status: str
    channels: list[str]
    factory_hint: dict | None
    created_at: datetime


class ActivityItem(BaseModel):
    robot_name: str
    message: str
    status: str
    created_at: datetime


class ExceptionItem(BaseModel):
    id: int
    type: str
    description: str
    status: str
    severity: str
    created_at: datetime


class DashboardResponse(BaseModel):
    metrics: list[MetricCard]
    pipeline: list[PipelineStage]
    products: list[ProductRow]
    activity: list[ActivityItem]
    exceptions: list[ExceptionItem]


class TriggerResponse(BaseModel):
    task_name: str
    status: str


class StorefrontProduct(BaseModel):
    id: int
    product_name: str
    source: str
    status: str
    price: float
    compare_at_price: float | None
    margin: float
    channels: list[str]
    factory_hint: dict | None
    badge: str
    subtitle: str
    image_tone: str


class InfluencerCard(BaseModel):
    platform: str
    handle: str
    title: str
    stats: str
    theme: str


class StorefrontResponse(BaseModel):
    products: list[StorefrontProduct]
    hero_product: StorefrontProduct | None
    influencer_cards: list[InfluencerCard]
    total_products: int
    updated_label: str


class CheckoutRequest(BaseModel):
    email: str = "buyer@example.com"


class CheckoutResponse(BaseModel):
    order_id: int
    product_name: str
    revenue: float
    supplier: str
    tracking_number: str | None
    status: str


class VoiceAssistantRequest(BaseModel):
    question: str


class VoiceAssistantResponse(BaseModel):
    answer: str
    audio_base64: str | None = None
