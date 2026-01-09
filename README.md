# 📊 Prometheus Metrics Lab
End-to-End Application Observability with Prometheus & Grafana

## 📌 Overview
This project demonstrates how to instrument a Python web application with Prometheus metrics, scrape those metrics using Prometheus, and visualize real-time service health using Grafana.
The application simulates realistic production behavior such as:
- steady traffic
- latency jitter
- error rates
- deployments
- outages
- feature flag toggles

This enables full observability of the four **SRE Golden Signals**:
**traffic**, **errors**, **latency**, and **saturation**.

## 🧠 What This Project Demonstrates
- Instrumenting application code with Prometheus **Counters**, **Gauges**, and **Histograms**
- Exposing a `/metrics` endpoint for scraping
- Configuring Prometheus scrape targets
- Writing real **PromQL queries**
- Building production-style **Grafana dashboards**
- Understanding what metrics mean, not just how to collect them

This mirrors how real DevOps / SRE teams monitor services in production.

## 🏗️ Architecture
```
Flask Application
  └── Exposes /metrics
          ↓
Prometheus
  └── Scrapes metrics every 5s
          ↓
Grafana
  └── Visualizes traffic, errors, latency, and deploy impact
```

## 📂 Project Structure
```
prometheus-metrics-lab/
├── app.py              # Instrumented Flask application
├── traffic_gen.py      # Generates realistic traffic & errors
├── prometheus.yml      # Prometheus scrape configuration
├── requirements.txt    # Python dependencies
├── venv/               # Python virtual environment
└── screenshots/        # Dashboard & Prometheus screenshots
```

## 🚀 Getting Started
1️⃣ Set up the environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2️⃣ Run the application
```
python app.py
```
Endpoints:
- App: http://localhost:8000
- Metrics: http://localhost:8000/metrics

3️⃣ Run Prometheus
```
prometheus --config.file=prometheus.yml
```
Prometheus UI:
```
http://localhost:9090
```
4️⃣ Run Grafana
```
grafana-server
```
Grafana UI:
```
http://localhost:3000
```
Default login:
```
admin / admin
```
5️⃣ Generate traffic
```
python traffic_gen.py
```
This generates:
- continuous traffic
- latency variation
- errors
- deploy-related degradation

## 📈 Metrics Collected

| Metric                          | Type      | Purpose                         |
| ------------------------------- | --------- | ------------------------------- |
| `http_requests_total`           | Counter   | Total traffic by route & status |
| `http_errors_total`             | Counter   | Error tracking                  |
| `http_request_duration_seconds` | Histogram | Latency percentiles             |
| `http_inprogress_requests`      | Gauge     | Concurrent load                 |
| `deployments_total`             | Counter   | Deploy correlation              |
| `feature_flag_enabled`          | Gauge     | Runtime configuration state     |


## 🔎 Prometheus Verification (Required Proof)

Prometheus screenshots are included only to prove scraping and ingestion.
Grafana dashboards provide the operational insight.

✅ Prometheus Targets (REQUIRED)
📍 URL:
```
http://localhost:9090/targets
```
This screenshot confirms:
- Prometheus is running
- The application target is UP
- `/metrics` is being scraped successfully

📸 Screenshot:

screenshots/prometheus-targets.png

➕ Prometheus Query Validation (Optional)
📍 URL:
```
http://localhost:9090/graph
```
Query:
```
rate(http_requests_total[1m])
```
This shows:
- Metrics exist in Prometheus
- PromQL queries return live data

📸 Screenshot:

screenshots/prometheus-traffic-rate.png

## 📊 Grafana Dashboards (Primary Focus)
Grafana dashboards tell the service health story and are the main visual artifacts.

✅ Required Panels & Screenshots

1️⃣ Request Throughput (Traffic)
```
rate(http_requests_total[1m])
```
📸 Screenshot:

screenshots/grafana-traffic-rate.png


2️⃣ Traffic by Status Code
```
sum by (status) (rate(http_requests_total[1m]))
```
📸 Screenshot:

screenshots/grafana-traffic-by-status.png

3️⃣ Error Rate (%)
```
sum(rate(http_requests_total{status="500"}[1m]))
/
sum(rate(http_requests_total[1m]))
```
📸 Screenshot:

screenshots/grafana-error-rate.png

4️⃣ Latency (p95)
```
histogram_quantile(
  0.95,
  sum(rate(http_request_duration_seconds_bucket[1m])) by (le)
)
```
📸 Screenshot:

screenshots/grafana-latency-p95.png

## 🧾 Summary

This project demonstrates end-to-end application observability using **Prometheus and Grafana** by instrumenting a Python web service with production-grade metrics and visualizing real-time system health. 

The lab simulates realistic service behavior—including traffic fluctuations, latency spikes, error conditions, and deployment impact—to showcase how DevOps and SRE teams monitor, analyze, and troubleshoot applications in production environments.

Through custom Prometheus metrics, validated scrape targets, PromQL queries, and Grafana dashboards, this project emphasizes **understanding what metrics represent**, not just how to collect them. 

It highlights practical monitoring concepts such as the **SRE Golden Signals**, deploy correlation, and operational visibility, reflecting real-world observability practices used in modern cloud-native systems
