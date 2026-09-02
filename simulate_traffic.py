import time
import random
import requests

URL = "http://localhost:8000/predict"

print("🚀 در حال ارسال درخواست‌های تست به مدل... (برای توقف Ctrl+C را بزنید)")

for i in range(50):
    # تولید تصادفی داده‌های تراکنش (بعضی نرمال، بعضی مشکوک)
    is_suspicious = random.random() < 0.3  # ۳۰ درصد احتمال تقلب
    
    if is_suspicious:
        payload = {
            "user_id": f"player_{random.randint(100, 999)}",
            "bet_amount": round(random.uniform(250.0, 800.0), 2),
            "bets_per_minute": random.randint(25, 45),
            "loss_streak": random.randint(7, 12),
            "ip_country_changed": 1
        }
    else:
        payload = {
            "user_id": f"player_{random.randint(100, 999)}",
            "bet_amount": round(random.uniform(5.0, 50.0), 2),
            "bets_per_minute": random.randint(1, 8),
            "loss_streak": random.randint(0, 3),
            "ip_country_changed": 0
        }
        
    res = requests.post(URL, json=payload)
    if res.status_code == 200:
        data = res.json()
        status_icon = "🚨 FRAUD" if data["is_fraud"] else "✅ NORMAL"
        print(f"[{i+1}/50] User: {data['user_id']} | Status: {status_icon} | Prob: {data['fraud_probability']}")
    time.sleep(0.2)

print("🎉 تمام ۵۰ تراکنش تست با موفقیت ارسال شدند!")
