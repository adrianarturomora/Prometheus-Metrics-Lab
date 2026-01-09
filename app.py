#Flask is used to create the web application
# Response lets us manually return raw HTTP responses (used for /metrics)
from flask import Flask, Response


# Prometheus client primitives
# Counter -> monotonically increasing values (requests, error, deploys)
# Gauge -> values that go up AND down (in-flight requests, flags)
# Histogram -> distributions (latency percentiles)
from prometheus_client import (
    Counter, Histogram, Gauge,
    generate_latest, CONTENT_TYPE_LATEST
)

# Use for timing requests and simulating latency
import time

# Used to simulate randomness (errors, itter, outages)
import random

app = Flask(__name__)

# Core “real service” metrics
REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["route", "method", "status"])
INPROGRESS = Gauge("http_inprogress_requests", "In-progress HTTP requests", ["route"])
LATENCY = Histogram("http_request_duration_seconds", "Request duration in seconds", ["route"])

# “Incidents” / badness signals
ERRORS = Counter("http_errors_total", "Total error responses", ["route", "status"])
DEPLOYMENTS = Counter("deployments_total", "Simulated deployments")
FEATURE_FLAGS = Gauge("feature_flag_enabled", "Feature flag state", ["flag"])

# Simulation knobs (pretend prod behavior)
STATE = {
    "error_rate": 0.02,     # 2% baseline errors
    "slow_mode": 0.0,       # extra latency seconds
    "outage": False
}

FEATURE_FLAGS.labels(flag="new_checkout").set(0)

@app.route("/")
def home():
    route = "/"
    INPROGRESS.labels(route=route).inc()
    start = time.time()

    try:
        # Outage simulation
        if STATE["outage"]:
            REQUESTS.labels(route=route, method="GET", status="503").inc()
            ERRORS.labels(route=route, status="503").inc()
            return "Service Unavailable\n", 503

        # Latency: baseline + jitter + optional slow_mode
        base = random.uniform(0.02, 0.12)
        jitter = random.uniform(0.0, 0.05)
        time.sleep(base + jitter + STATE["slow_mode"])

        # Error simulation
        if random.random() < STATE["error_rate"]:
            REQUESTS.labels(route=route, method="GET", status="500").inc()
            ERRORS.labels(route=route, status="500").inc()
            return "Internal Server Error\n", 500

        REQUESTS.labels(route=route, method="GET", status="200").inc()
        return "Prometheus Metrics Lab\n", 200

    finally:
        LATENCY.labels(route=route).observe(time.time() - start)
        INPROGRESS.labels(route=route).dec()


# Admin endpoints to emulate “ops events”
@app.route("/admin/deploy", methods=["POST"])
def deploy():
    # A deploy often causes a short latency bump & transient errors
    DEPLOYMENTS.inc()
    STATE["slow_mode"] = min(STATE["slow_mode"] + 0.15, 1.5)
    STATE["error_rate"] = min(STATE["error_rate"] + 0.03, 0.25)
    return "deploy simulated\n", 200

@app.route("/admin/recover", methods=["POST"])
def recover():
    # Recovery brings system back to baseline
    STATE["slow_mode"] = 0.0
    STATE["error_rate"] = 0.02
    STATE["outage"] = False
    return "recovered\n", 200

@app.route("/admin/outage", methods=["POST"])
def outage():
    STATE["outage"] = True
    return "outage simulated\n", 200

@app.route("/admin/flag/<name>/<int:value>", methods=["POST"])
def flag(name, value):
    FEATURE_FLAGS.labels(flag=name).set(1 if value else 0)
    return f"flag {name} set to {value}\n", 200


@app.route("/metrics")
def metrics():
    data = generate_latest()
    return Response(data, mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
