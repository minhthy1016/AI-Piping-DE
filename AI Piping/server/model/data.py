from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from beanie import Document, init_beanie
import motor.motor_asyncio
from typing import Optional, List
from uuid import uuid4
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime


app = FastAPI()

class Lead(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    status: int = 0
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None

    class Settings:
        name = "Lead_collection"

class Persona(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    lead_id: str
    academic_field: Optional[str] = None
    company_type: Optional[str] = None

    class Settings:
        name = "Pesona_collection"