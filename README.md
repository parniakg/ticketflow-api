# TicketFlow API

A clean, modular RESTful API for event ticket management and booking, built with **FastAPI** and **SQLAlchemy**.

## Features
- **User Management:** Register new users with unique username validation.
- **Event & Ticket Management:** Create and list available event tickets.
- **Ticket Booking System:** Purchase tickets linked to specific users (`ForeignKey` relationship) with double-booking prevention.
- **Interactive API Docs:** Built-in Swagger UI documentation.

## Tech Stack
- **Framework:** FastAPI
- **Database & ORM:** SQLite, SQLAlchemy
- **Validation:** Pydantic

## How to Run Locally
1. Install dependencies:
   pip install -r requirements.txt

2. Run the server:
   uvicorn main:app --reload

3. Open your browser and visit `http://127.0.0.1:8000/docs` to test the endpoints.