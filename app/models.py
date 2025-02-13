# app/models.py
from typing import Optional
from sqlmodel import SQLModel, Field
import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    role: str

class ChatHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    question: str
    answer: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
