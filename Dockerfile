# ۱. استفاده از ایمیج پایه سبک و رسمی پایتون
FROM python:3.11-slim

# ۲. مشخص کردن پوشه کاری درون کانتینر
WORKDIR /app

# ۳. جلوگیری از نوشتن فایل‌های .pyc و بافر شدن لاگ‌ها
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ۴. کپی کردن لیست نیازمندی‌ها و نصب آن‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ۵. کپی کردن کدهای برنامه و مدل آموزش‌دیده به داخل کانتینر
COPY src/ ./src/
COPY models/ ./models/

# ۶. باز کردن پورت سرویس
EXPOSE 8000

# ۷. دستور نهایی برای اجرای سرور در حالت پروداکشن
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
