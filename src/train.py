import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os

def generate_mock_igaming_data(n_samples: int = 10000) -> pd.DataFrame:
    """
    تولید داده‌های شبیه‌سازی‌شده تراکنش‌های شرط‌بندی
    """
    np.random.seed(42)
    
    # متغیرها (Features):
    # ۱. مبلغ شرط (دلار)
    bet_amount = np.random.exponential(scale=25, size=n_samples) + 1
    # ۲. تعداد کلیک/شرط در هر دقیقه (سرعت مشکوک نشان‌دهنده ربات است)
    bets_per_minute = np.random.poisson(lam=8, size=n_samples)
    # ۳. نسبت باخت‌های پشت‌سرهم قبل از این شرط
    loss_streak = np.random.geometric(p=0.3, size=n_samples) - 1
    # ۴. آیا IP یا کشور در یک ساعت اخیر تغییر کرده؟ (0: خیر, 1: بله)
    ip_country_changed = np.random.choice([0, 1], size=n_samples, p=[0.92, 0.08])
    
    # ساخت تارگت (قانون تقلب شبیه‌سازی‌شده)
    fraud_risk_score = (
        (bet_amount > 120).astype(int) * 0.35 +
        (bets_per_minute > 20).astype(int) * 0.40 +
        (ip_country_changed == 1).astype(int) * 0.30 +
        (loss_streak > 6).astype(int) * 0.15
    )
    # برچسب تقلب (0: نرمال, 1: مشکوک/تقلب)
    is_fraud = (fraud_risk_score >= 0.50).astype(int)
    
    df = pd.DataFrame({
        "bet_amount": bet_amount,
        "bets_per_minute": bets_per_minute,
        "loss_streak": loss_streak,
        "ip_country_changed": ip_country_changed,
        "is_fraud": is_fraud
    })
    return df

def train_and_save_model():
    print("🚀 در حال تولید دیتا و آموزش مدل...")
    df = generate_mock_igaming_data()
    
    X = df.drop(columns=["is_fraud"])
    y = df["is_fraud"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # آموزش مدل سبک
    model = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42)
    model.fit(X_train, y_train)
    
    # ارزیابی
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    print("\n📊 گزارش ارزیابی مدل:")
    print(classification_report(y_test, preds))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, probs):.4f}")
    
    # ذخیره مدل
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "fraud_model.joblib")
    joblib.dump(model, model_path)
    print(f"\n✅ مدل با موفقیت در مسیر '{model_path}' ذخیره شد.")

if __name__ == "__main__":
    train_and_save_model()
