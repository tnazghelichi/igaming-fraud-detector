\# 🎰 Real-Time iGaming Fraud Detection Engine



\[!\[iGaming Fraud Detection CI](https://github.com/tnazghelichi/

igaming-fraud-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/tnazghelichi/

igaming-fraud-detector/actions/workflows/ci.yml)

!\[Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)

!\[FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)

!\[Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)

!\[Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange.svg)



An end-to-end, production-grade Machine Learning system designed for sub-50ms fraud detection in high-throughput iGaming platforms (e.g., automated bot detection, multi-accounting, bonus abuse).



\---



\## 📌 Architecture Overview

```text

\[ Incoming Bets / Actions ]

│

▼

┌─────────────────┐

│  FastAPI Engine │ ◄── (Loads Random Forest model from /models)

│  (Port 8000)    │ ─── Exposes /predict and /metrics

└────────┬────────┘

│

Prometheus Scraping (Port 9090)

│

▼

┌─────────────────┐

│ Grafana Dashboard│ (Port 3000) - Real-time alerts, TPS, \& Fraud Rate

└─────────────────┘


Key Features & Engineering Highlights
Low-Latency Inference: Sub-50ms response time per prediction with an optimized scikit-learn feature pipeline.
Observability & MLOps: Integrated Prometheus metric instrumentation and Grafana dashboards for real-time fraud rate and system throughput monitoring.
Robust CI Pipeline: GitHub Actions workflow running automated unit tests (pytest) and Docker build validation on every push.
Containerized Microservices: Multi-container orchestration powered by docker-compose.
🛠️ Tech Stack
ML Core: Scikit-Learn (Random Forest Classifier), NumPy, Pandas
API Framework: FastAPI, Uvicorn, Pydantic
Testing & Quality: Pytest, HTTPX
Containerization: Docker, Docker Compose
Monitoring & Metrics: Prometheus, Grafana
CI Automation: GitHub Actions (YAML)

