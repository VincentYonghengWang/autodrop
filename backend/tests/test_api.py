from __future__ import annotations

from sqlalchemy import select

from app.models import Order
from app.services.demo_seed import seed_demo_data


def test_health_and_dashboard_endpoints(client, db_session) -> None:
    seed_demo_data(db_session)

    health_response = client.get("/api/health")
    assert health_response.status_code == 200
    assert health_response.json() == {"status": "ok"}

    dashboard_response = client.get("/api/dashboard")
    assert dashboard_response.status_code == 200

    payload = dashboard_response.json()
    assert len(payload["metrics"]) == 4
    assert len(payload["pipeline"]) == 5
    assert len(payload["products"]) >= 3
    assert payload["products"][0]["product_name"]
    assert payload["activity"]
    assert payload["exceptions"]


def test_storefront_and_checkout_endpoints(client, db_session) -> None:
    seed_demo_data(db_session)

    storefront_response = client.get("/api/storefront")
    assert storefront_response.status_code == 200

    storefront_payload = storefront_response.json()
    assert storefront_payload["hero_product"]["product_name"]
    assert storefront_payload["products"]

    product_id = storefront_payload["products"][0]["id"]
    response = client.post(f"/api/storefront/checkout/{product_id}", json={"email": "demo@example.com"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["product_name"] == storefront_payload["products"][0]["product_name"]
    assert payload["status"] == "confirmed"
    assert db_session.scalar(select(Order.id).where(Order.id == payload["order_id"])) is not None


def test_trigger_endpoint_runs_in_demo_mode(client, db_session) -> None:
    response = client.post("/api/triggers/trend-radar")
    assert response.status_code == 200
    assert response.json() == {"task_name": "trend_radar", "status": "completed"}

    demo_response = client.post("/api/demo/run-all")
    assert demo_response.status_code == 200
    assert demo_response.json() == {"task_name": "demo_run_all", "status": "completed"}
