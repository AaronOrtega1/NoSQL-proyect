#!/usr/bin/env python3
import argparse
import logging
import os
import requests


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('flights.log')
handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
FLIGHTS_API_URL = os.getenv("FLIGHTS_API_URL", "http://localhost:27017")
    
def get_month_count():
    suffix = "/month-count"
    endpoint = FLIGHTS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print(json_resp)
    else: print(f"Error: {response}")

def main():
    log.info(f"Welcome to flights catalog. App requests to: {FLIGHTS_API_URL}")
    get_month_count()
        
if __name__ == "__main__":
    main()
