#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Flight, FlightUpdate

router = APIRouter()


@router.post("/", response_description="Post a new flight", status_code=status.HTTP_201_CREATED, response_model=Flight)
def create_flight(request: Request, flight: Flight = Body(...)):
    flight = jsonable_encoder(flight)
    new_flight = request.app.database["flights"].insert_one(flight)
    created_flight = request.app.database["flights"].find_one(
        {"_id": new_flight.inserted_id}
    )

    return created_flight


@router.get("/destinations/most_flights", response_description="Get all flights by destination", response_model=List[Flight])
async def get_destination_with_num_flights(request: Request, to: str = "", day: int = 0, month: int = 0, year: int = 0, limit: int = 0, skip: int = 0):

    num_flights_by_destination_and_month = list(request.app.database["flight"].aggregate([
        {"$group": {"_id": {"destination": "$to", "month": {
            "$month": "$departure_date"}}, "total_flights": {"$sum": 1}}},
        {"$sort": {"total_flights": DESCENDING}}
    ]))

    result = []
    for flight in num_flights_by_destination_and_month:
        result.append({
            "destination": flight["_id"]["destination"],
            "month": flight["_id"]["month"],
            "num_flights": flight["total_flights"]
        })

    return result


@router.get("/", response_description="Get all flights by destination", response_model=List[Flight])
def flight(request: Request, to: str = "", day: int = 0, month: int = 0, year: int = 0, limit: int = 0, skip: int = 0):
    flight = list(request.app.database["flight"].find())
    flight_by_destiny = list(
        request.app.database["flight"].find({"destiny": to}))
    flight_by_day = list(request.app.database["flight"].find({"day": day}))
    flight_by_month = list(
        request.app.database["flight"].find({"month": month}))
    flight_by_year = list(request.app.database["flight"].find({"month": year}))

    if (to != ""):
        return flight_by_destiny
    elif (day != 0):
        return flight_by_day
    elif (month != 0):
        return flight_by_month
    elif (year != 0):
        return flight_by_year
    else:
        return flight


@router.get("/{id}", response_description="Get a single flight by id", response_model=Flight)
def find_flight(id: str, request: Request):
    if (flight := request.app.database["flights"].find_one({"_id": id})) is not None:
        return flight

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Flight with ID {id} not found")


@router.put("/{id}", response_description="Update a flight by id", response_model=Flight)
def update_flight(id: str, request: Request, flight: FlightUpdate = Flight(...)):
    if (request.app.database["flights"].find_one({"_id": id})) is not None:
        my_query = {"_id": id}
        updated_flight = flight.dict(exlude_unset=True)
        new_values = {"$set": {updated_flight}}
        request.app.database["flights"].update_one(my_query, new_values)
        return updated_flight

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Flight with ID {id} not found")


@router.delete("/{id}", response_description="Delete a flight")
def delete_flight(id: str, request: Request, response: Response):
    if (request.app.database["flights"].find_one({"_id": id})) is not None:
        my_query = {"_id": id}
        request.app.database["flights"].delete_one(my_query)
        response.status_code = status.HTTP_204_NO_CONTENT

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Flight with ID {id} not found")
