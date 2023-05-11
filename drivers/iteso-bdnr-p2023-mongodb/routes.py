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
    
@router.get("/month-count")
async def get_month_count(request: Request):
    """
    Devuelve un conteo de los meses del más repetido al menos repetido.
    """
    # Buscar todos los vuelos en la base de datos y obtener su mes
    months = list(request.app.database.flights.find({}, {"month": 1, "_id": 0}))

    # Contar la cantidad de veces que aparece cada mes
    month_counts = {}
    for month in months:
        month_num = int(month["month"])
        if month_num not in month_counts:
            month_counts[month_num] = 1
        else:
            month_counts[month_num] += 1

    # Ordenar los meses por cantidad de veces que aparecen
    sorted_months = sorted(month_counts.items(), key=lambda x: x[1], reverse=True)

    # Devolver el resultado
    return {
        "month_count": [
            {"month": str(month[0]), "count": month[1]} for month in sorted_months
        ]
    }
