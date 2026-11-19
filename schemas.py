from pydantic import BaseModel

class TicketCreate(BaseModel):
    event: str
    price: int

class UserCreate(BaseModel):
    username: str
    email: str