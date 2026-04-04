from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "AutoDrop"
    environment: str = "development"
    api_v1_str: str = "/api"
    secret_key: str = "change-me"
    admin_password: str = "autodrop-admin"
    backend_cors_origins: str = "http://localhost:5173"

    database_url: str = "sqlite:///./autodrop.db"
    redis_url: str = "redis://redis:6379/0"
    demo_mode: bool = True

    margin_floor: float = 0.20
    viral_score_threshold: int = 60
    product_test_window_days: int = 5
    min_orders_for_winner: int = 10
    min_revenue_for_winner: int = 200
    default_markup_factor: float = 3.0
    ad_spend_estimate_pct: float = 0.15
    admin_email: str = "owner@example.com"

    tiktok_api_key: str = ""
    tiktok_access_token: str = ""
    instagram_access_token: str = ""
    instagram_business_account_id: str = ""
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    shopify_api_key: str = ""
    shopify_store_domain: str = ""
    amazon_sp_api_refresh_token: str = ""
    amazon_lwa_app_id: str = ""
    amazon_lwa_client_secret: str = ""
    cj_dropshipping_api_key: str = ""
    aliexpress_api_key: str = ""
    aliexpress_secret: str = ""
    runwayml_api_key: str = ""
    remove_bg_api_key: str = ""
    sendgrid_api_key: str = ""
    easypost_api_key: str = ""

    @computed_field
    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
