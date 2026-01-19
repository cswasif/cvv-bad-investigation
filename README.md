# CVV-BAD Investigation - Hyperswitch

This repository hosts attack scripts and CI configurations to test the CVV validation logic of the [Hyperswitch](https://github.com/juspay/hyperswitch) payment switch.

## Experiments

### Experiment A: CVV Enumeration
- File: `cvv_enumerator.py`
- Goal: Brute-force the CVV field to check for rate limiting.

### Experiment C: Null Bypass
- File: `cvv_bypass_null.py`
- Goal: Send requests with `null`, empty, or missing CVV fields to check for optional value bypasses.

## Running
These experiments run automatically in GitHub Actions against a fresh instance of Hyperswitch (Docker).
