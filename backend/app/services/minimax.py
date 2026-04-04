from __future__ import annotations

import json
from urllib import error, request

from app.core.config import get_settings

settings = get_settings()

MINIMAX_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"


def _post_minimax(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        MINIMAX_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {settings.minimax_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def generate_product_copy(product_name: str, source: str | None = None, factory_hint: dict | None = None) -> dict | None:
    if not settings.minimax_api_key:
        return None

    source_text = source or "social commerce trend feeds"
    factory_text = ""
    if factory_hint and factory_hint.get("city") and factory_hint.get("category"):
        factory_text = (
            f" Factory clue: sourced via {factory_hint['city']} for {factory_hint['category']}."
        )

    prompt = (
        f"Write high-converting ecommerce copy for this product: {product_name}. "
        f"It was detected from {source_text}.{factory_text} "
        "Return strict JSON with this schema only: "
        '{"shopify_title":"",'
        '"shopify_description_html":"",'
        '"tiktok_title":"",'
        '"tiktok_hashtags":[""],'
        '"instagram_captions":["",""]}. '
        "Keep Shopify description concise, benefits-led, and safe for a consumer storefront."
    )

    payload = {
        "model": settings.minimax_model,
        "messages": [
            {"role": "system", "name": "MiniMax AI", "content": "You are an expert ecommerce copywriter."},
            {"role": "user", "name": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 600,
    }

    try:
        response = _post_minimax(payload)
        content = response["choices"][0]["message"]["content"]
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1:
            return None
        return json.loads(content[start : end + 1])
    except (KeyError, IndexError, json.JSONDecodeError, error.URLError, TimeoutError, ValueError):
        return None
