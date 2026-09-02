import joblib
import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

# مدل ذخیره‌شده در این متغیر سراسری در RAM نگه داشته می‌شود
ml_models = {}

# متریک اختصاصی Prometheus: شمارش تعداد تراکنش‌های عادی و مشکوک به تقلب
FRAUD_COUNTER = Counter(
    "igaming_fraud_predictions_total",
    "تعداد پیش‌بینی‌های انجام شده به تفکیک تقلب یا سالم",
    ["is_fraud", "risk_level"]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ۱. بارگذاری مدل هنگام استارت‌آپ سرویس
    try:
        ml_models["fraud_model"] = joblib.load("models/fraud_model.joblib")
        print("✅ مدل با موفقیت در حافظه رم لود شد.")
    except Exception as e:
        print(f"❌ خطا در بارگذاری مدل: {e}")
        ml_models["fraud_model"] = None
    yield
    # ۲. پاک‌سازی رم هنگام خاموش شدن
    ml_models.clear()

app = FastAPI(
    title="iGaming Real-Time Fraud Detection Engine",
    description="سرویس بلادرنگ تشخیص رفتارهای مشکوک و تقلب در پلتفرم شرط‌بندی",
    version="1.0.0",
    lifespan=lifespan
)

# فعال‌سازی ابزار مانیتورینگ Prometheus روی اندپوینت /metrics
Instrumentator().instrument(app).expose(app)

class TransactionRequest(BaseModel):
    user_id: str = Field(..., description="شناسه یکتای کاربر")
    bet_amount: float = Field(..., gt=0, description="مبلغ شرط (دلار)")
    bets_per_minute: int = Field(..., ge=0, description="سرعت شرط‌بندی در دقیقه")
    loss_streak: int = Field(..., ge=0, description="تعداد باخت‌های پیاپی اخیر")
    ip_country_changed: int = Field(..., ge=0, le=1, description="تغییر کشور آی‌پی (0 یا 1)")

class PredictionResponse(BaseModel):
    user_id: str
    is_fraud: bool
    fraud_probability: float
    risk_level: str

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    if ml_models.get("fraud_model") is None:
        raise HTTPException(status_code=503, detail="Model is not ready")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
def predict_fraud(transaction: TransactionRequest):
    model = ml_models.get("fraud_model")
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")
    
    input_data = pd.DataFrame([{
        "bet_amount": transaction.bet_amount,
        "bets_per_minute": transaction.bets_per_minute,
        "loss_streak": transaction.loss_streak,
        "ip_country_changed": transaction.ip_country_changed
    }])
    
    # استنتاج با مدل
    fraud_prob = float(model.predict_proba(input_data)[0][1])
    is_fraud = bool(fraud_prob >= 0.5)
    
    # دسته‌بندی سطح ریسک
    if fraud_prob < 0.3:
        risk_level = "LOW"
    elif fraud_prob < 0.7:
        risk_level = "MEDIUM"
    elif fraud_prob < 0.9:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"
        
    # ثبت آمار در Prometheus
    FRAUD_COUNTER.labels(is_fraud=str(is_fraud), risk_level=risk_level).inc()
    
    return PredictionResponse(
        user_id=transaction.user_id,
        is_fraud=is_fraud,
        fraud_probability=round(fraud_prob, 4),
        risk_level=risk_level
    )
