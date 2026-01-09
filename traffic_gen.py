import time
import random
import requests
import threading

BASE = "http://localhost:8000"

def hit_root():
    try:
        requests.get(f"{BASE}/", timeout=2)
    except Exception:
        pass

def post(path):
    try:
        requests.post(f"{BASE}{path}", timeout=2)
    except Exception:
        pass

def traffic_loop():
    """
    Emulates a day-in-the-life traffic pattern:
    - baseline steady traffic
    - occasional spikes
    - occasional error bursts due to "deploys"
    - rare outage + recovery
    """
    phase = "baseline"
    phase_until = time.time() + 60

    while True:
        now = time.time()

        # Choose a new phase every 30–90 seconds
        if now >= phase_until:
            phase = random.choices(
                ["baseline", "spike", "deploy", "outage"],
                weights=[70, 20, 8, 2],
                k=1
            )[0]
            phase_until = now + random.randint(30, 90)

            # Trigger ops events
            if phase == "deploy":
                post("/admin/deploy")
            elif phase == "outage":
                post("/admin/outage")
                # auto-recover after a short outage window
                threading.Timer(random.randint(10, 25), lambda: post("/admin/recover")).start()

        # Traffic intensity by phase
        if phase == "baseline":
            rps = random.uniform(2, 6)
        elif phase == "spike":
            rps = random.uniform(15, 35)
        elif phase == "deploy":
            rps = random.uniform(4, 10)
        else:  # outage
            rps = random.uniform(1, 3)

        # Fire N requests this second
        n = max(1, int(rps))
        for _ in range(n):
            threading.Thread(target=hit_root, daemon=True).start()

        time.sleep(1)

if __name__ == "__main__":
    print("Generating realistic traffic + incidents against", BASE)
    traffic_loop()
