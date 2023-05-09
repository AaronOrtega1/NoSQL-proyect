#!/usr/bin/env python3
import csv
import requests

BASE_URL = "http://localhost:8000"


def main():
    with open("fligh_passangers.csv") as fd:
        flights_csv = csv.DictReader(fd)
        for flight in flights_csv:
            del flight["flightID"]
            flight["airlines"] = flight["airlines"].split("/")
            x = requests.post(BASE_URL+"/flight", json=flight)
            if not x.ok:
                print(f"Failed to post flight {x} - {flight}")


if __name__ == "__main__":
    main()
