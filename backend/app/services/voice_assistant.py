from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ProductCandidate, TrendSignal
from app.services.elevenlabs import text_to_speech_base64


def _format_product(product: ProductCandidate, signal: TrendSignal | None) -> str:
    source = signal.source.title() if signal else "our trend engine"
    supplier = product.supplier_name
    return (
        f"{product.product_name} is currently priced at ${product.sell_price:.2f}, "
        f"with an estimated margin of {round(product.margin * 100)} percent. "
        f"We spotted it on {source} and fulfill it through {supplier}."
    )


def build_voice_reply(question: str, db: Session) -> dict:
    products = db.scalars(select(ProductCandidate).order_by(ProductCandidate.created_at.desc()).limit(8)).all()
    lowered = question.lower()

    matched = None
    for product in products:
        if product.product_name.lower() in lowered:
            matched = product
            break

    if matched:
        signal = db.scalar(select(TrendSignal).where(TrendSignal.product_name == matched.product_name).limit(1))
        answer = _format_product(matched, signal)
    elif "best" in lowered or "winner" in lowered:
        winner = next((product for product in products if product.status == "winner"), None)
        if winner:
            signal = db.scalar(select(TrendSignal).where(TrendSignal.product_name == winner.product_name).limit(1))
            answer = f"Our current winner is {_format_product(winner, signal)}"
        else:
            answer = "Right now we do not have a winner flagged, but we are actively testing products from the live catalog."
    elif "shipping" in lowered or "delivery" in lowered:
        answer = (
            "For the demo store, products ship from verified factory partners in China, "
            "and we present them as 7 to 14 day delivery items with automated routing."
        )
    else:
        summary = ", ".join(product.product_name for product in products[:3])
        answer = (
            f"Here are the top products in the store right now: {summary}. "
            "Ask me about price, margin, trend source, or shipping and I can walk you through each one."
        )

    audio_base64 = text_to_speech_base64(answer)
    return {"answer": answer, "audio_base64": audio_base64}
