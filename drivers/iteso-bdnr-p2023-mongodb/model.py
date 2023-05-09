#!/usr/bin/env python3
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Flight(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airline: str = Field(...)
    origin: str = Field(...)
    to: str = Field(...)
    day: int = Field(...)
    month: int = Field(...)
    year: int = Field(...)
    gender: str = Field(...)
    reason: str = Field(...)
    stay: str = Field(...)
    transit: str = Field(...)
    connection: bool = Field(...)
    wait: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "airline": "Alask",
                "origin": "LAX",
                "to": "GDL",
                "day": 2,
                "month": 2,
                "year": 2023,
                "gender": "male",
                "reason": "Business/Work",
                "stay": "Home",
                "transit": "Public Transportation",
                "connection": True,
                "wait": 127
            }
        }


class FlightUpdate(BaseModel):
    airline: Optional[str]
    origin: Optional[str]
    to: Optional[str]
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]
    gender: Optional[str]
    reason: Optional[str]
    stay: Optional[str]
    transit: Optional[str]
    connection:  Optional[bool]
    wait: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "airline": "Alask",
                "origin": "LAX",
                "to": "GDL",
                "day": 2,
                "month": 2,
                "year": 2023,
                "gender": "male",
                "reason": "Business/Work",
                "stay": "Home",
                "transit": "Public Transportation",
                "connection": True,
                "wait": 127
            }
        }
