from pathlib import Path
from typing import Any, Dict, List

import pickledb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class Flight(BaseModel):
    flight_id: str
    origin: str
    destination: str
    departure: str
    arrival: str
    price: float


class BookingRequest(BaseModel):
    flight_id: int
    passenger_name: str
    passenger_email: str


DEFAULT_FLIGHTS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "flight_id": "ABC123",
        "origin": "New York (JFK)",
        "destination": "Los Angeles (LAX)",
        "departure": "2024-04-03T08:00:00",
        "arrival": "2024-04-03T11:30:00",
        "price": 200.00,
    },
    {
        "id": 2,
        "flight_id": "DEF456",
        "origin": "London (LHR)",
        "destination": "Tokyo (HND)",
        "departure": "2024-04-03T13:45:00",
        "arrival": "2024-04-04T08:20:00",
        "price": 500.00,
    },
    {
        "id": 3,
        "flight_id": "GHI789",
        "origin": "Dubai (DXB)",
        "destination": "Sydney (SYD)",
        "departure": "2024-04-03T22:30:00",
        "arrival": "2024-04-04T18:15:00",
        "price": 600.00,
    },
    {
        "id": 4,
        "flight_id": "JKL012",
        "origin": "Paris (CDG)",
        "destination": "Singapore (SIN)",
        "departure": "2024-04-03T09:15:00",
        "arrival": "2024-04-04T03:40:00",
        "price": 400.00,
    },
    {
        "id": 5,
        "flight_id": "MNO345",
        "origin": "Los Angeles (LAX)",
        "destination": "Mexico City (MEX)",
        "departure": "2024-04-03T16:30:00",
        "arrival": "2024-04-03T19:45:00",
        "price": 150.00,
    },
    {
        "id": 6,
        "flight_id": "PQR678",
        "origin": "Tokyo (HND)",
        "destination": "Seoul (ICN)",
        "departure": "2024-04-03T11:00:00",
        "arrival": "2024-04-03T13:25:00",
        "price": 100.00,
    },
]

FLIGHTS_KEY = "flights"
BOOKED_FLIGHTS_KEY = "booked_flights"
DB_PATH = Path(__file__).resolve().parent / "storage.db"
db = pickledb.PickleDB(str(DB_PATH))


async def _initialize_storage() -> None:
    existing_keys = set(await db.all())
    if FLIGHTS_KEY not in existing_keys:
        await db.set(FLIGHTS_KEY, DEFAULT_FLIGHTS.copy())
    if BOOKED_FLIGHTS_KEY not in existing_keys:
        await db.set(BOOKED_FLIGHTS_KEY, [])
    await db.save()


async def _get_flights() -> List[Dict[str, Any]]:
    return await db.get(FLIGHTS_KEY, [])


async def _set_flights(flights: List[Dict[str, Any]]) -> None:
    await db.set(FLIGHTS_KEY, flights)
    await db.save()


async def _get_booked_flights() -> List[Dict[str, Any]]:
    return await db.get(BOOKED_FLIGHTS_KEY, [])


async def _set_booked_flights(booked_flights: List[Dict[str, Any]]) -> None:
    await db.set(BOOKED_FLIGHTS_KEY, booked_flights)
    await db.save()


def reset_storage_for_tests() -> None:
    """Reset persistent storage to a known state for test isolation."""
    db.db = {
        FLIGHTS_KEY: DEFAULT_FLIGHTS.copy(),
        BOOKED_FLIGHTS_KEY: [],
    }
    db.save()


@app.on_event("startup")
async def startup_event() -> None:
    await db.load()
    await _initialize_storage()


@app.get("/flights")
async def get_flights():
    return await _get_flights()


@app.post("/flights")
async def add_flight(flight: Flight):
    flights = await _get_flights()
    new_flight = flight.model_dump()
    max_id = max((item["id"] for item in flights), default=0)
    new_flight["id"] = max_id + 1
    flights.append(new_flight)
    await _set_flights(flights)
    return {"message": "flight added"}


@app.post("/book-flight/", response_model=Flight)
async def book_flight(booking_request: BookingRequest):
    flights = await _get_flights()
    flight_id = booking_request.flight_id

    # Check if the flight exists
    flight = next((item for item in flights if item["id"] == flight_id), None)
    if flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")

    booked_flights = await _get_booked_flights()
    booked_flights.append(booking_request.model_dump())
    await _set_booked_flights(booked_flights)

    return flight


@app.get("/booked-flights", response_model=List[BookingRequest])
async def get_booked_flights():
    return await _get_booked_flights()