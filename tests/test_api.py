from fastapi.testclient import TestClient
from src.app import app
import pytest

client = TestClient(app)

def test_health_check_endpoint():
    """تست سلامت سرویس و اطمینان از اینکه مدل در رم لود شده است"""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["model_loaded"] is True

def test_fraud_prediction_high_risk():
    """تست ورودی مشکوک و اطمینان از خروجی تقلب (Fraud)"""
    payload = {
        "user_id": "suspect_01",
        "bet_amount": 300.0,
        "bets_per_minute": 35,
        "loss_streak": 9,
        "ip_country_changed": 1
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "suspect_01"
        assert data["is_fraud"] is True
        assert data["risk_level"] in ["HIGH", "CRITICAL"]

def test_invalid_input_validation():
    """تست ورودی نامعتبر (مبلغ منفی) و اطمینان از مسدود شدن با خطای ۴۲۲"""
    bad_payload = {
        "user_id": "player_bad",
        "bet_amount": -50.0, # مبلغ نامعتبر
        "bets_per_minute": 5,
        "loss_streak": 0,
        "ip_country_changed": 0
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=bad_payload)
        assert response.status_code == 422  # خطای اعتبارسنجی Pydantic
