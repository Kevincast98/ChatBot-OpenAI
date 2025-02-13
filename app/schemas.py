# app/schemas.py
from pydantic import BaseModel
import datetime

class UserCreate(BaseModel):
    username: str
    role: str

class Message(BaseModel):
    username: str
    message: str

class ChatResponse(BaseModel):
    answer: str

class ChatHistoryResponse(BaseModel):
    question: str
    answer: str
    timestamp: datetime.datetime
