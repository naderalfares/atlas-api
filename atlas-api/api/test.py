import pytest
from fastapi.testclient import TestClient
from .main import app, flights_db, booked_flights_db, Flight, BookingRequest

client = TestClient(app)

def test_get_flights():
    response = client.get("/flights")
    assert response.status_code == 200
    assert response.json() == flights_db

def test_add_flight():
    new_flight = {
        "flight_id": "TUV789",
        "origin": "Berlin (TXL)",
        "destination": "Rome (FCO)",
        "departure": "2024-05-01T10:00:00",
        "arrival": "2024-05-01T12:30:00",
        "price": 300.00
    }
    response = client.post("/flights", json=new_flight)
    assert response.status_code == 200
    assert response.json()["message"] == "flight added"
    assert len(flights_db) == 7

def test_book_flight():
    booking_request = {
        "flight_id": 1,
        "passenger_name": "John Doe",
        "passenger_email": "john@example.com"
    }
    response = client.post("/book-flight/", json=booking_request)
    assert response.status_code == 200
    assert len(booked_flights_db) == 1

def test_get_booked_flights():
    response = client.get("/booked-flights")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["flight_id"] == 1


