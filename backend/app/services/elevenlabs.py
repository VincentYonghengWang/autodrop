from __future__ import annotations

import base64
import json
from urllib import error, request

from app.core.config import get_settings

settings = get_settings()


def text_to_speech_base64(text: str) -> str | None:
    if not settings.elevenlabs_api_key or not text.strip():
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.elevenlabs_voice_id}"
    payload = {
        "text": text[:1500],
        "model_id": settings.elevenlabs_model_id,
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.75,
            "style": 0.25,
            "use_speaker_boost": True,
        },
    }
    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": settings.elevenlabs_api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            return base64.b64encode(response.read()).decode("utf-8")
    except (error.URLError, TimeoutError):
        return None
