from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from beanie import Document, init_beanie
import motor.motor_asyncio
from typing import Optional, List
from uuid import uuid4
from contextlib import asynccontextmanager
import asyncio
import mongomock
import requests
from server.model.data import Lead, Persona
import json

app = FastAPI()


# Define db connection
async def init_db():
    # client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    # Create a mock MongoDB client using mongomock
    client = mongomock.MongoClient()
    # Select the lead_db database within the mock MongoDB client
    db = client['lead_db']
    # Initialize Beanie with the mock database and Lead document model
    await init_beanie(database=db, document_models=[Lead, Persona])

@app.on_event("startup")
async def on_startup():
    await init_db()

# Get Linkedin data, then ETL
def get_linkedin_data(email: str, academic_field:str, company_type:str ) -> Optional[dict]:
    mock_data = {
        # "email":email,
        "academic_field": academic_field,
        "company_type": company_type
    }
    return mock_data

@app.post("/leads/{lead_id}/persona")
async def extract_transform_load(lead_id: str):
    email = await get_lead_email_by_id(lead_id)
    if email:
        linkedin_data = get_linkedin_data(email)
        if linkedin_data:
            persona = Persona(
                lead_id=lead_id,
                academic_field=linkedin_data.get("academic_field"),
                company_type=linkedin_data.get("company_type")
            )
            await persona.insert()
            return {"message": "Persona created"}
    raise HTTPException(status_code=404, detail="Lead not found or LinkedIn data unavailable")

# Endpoint to get persona details of a lead by lead_id
@app.get("/persona/{lead_id}", response_model=Persona)
async def get_persona_by_lead_id(lead_id: str):
    # Fetch the persona document from the database
    persona = await Persona.find_one(Persona.lead_id == lead_id)
    if persona:
        return persona
    raise HTTPException(status_code=404, detail="Persona not found")

@app.put("/persona/{lead_id}")
async def update_persona(lead_id: str, academic_field: Optional[str] = None, company_type: Optional[str] = None):
    persona = await Persona.find_one(Persona.lead_id == lead_id)
    if persona:
        if academic_field:
            persona.academic_field = academic_field
        if company_type:
            persona.company_type = company_type
        await persona.save()
        return {"message": "Persona updated"}
    raise HTTPException(status_code=404, detail="Persona not found")

@app.get("/personas", response_model=List[str])
async def get_lead_ids_by_persona(academic_field: Optional[str] = None, company_type: Optional[str] = None):
    query = {}
    if academic_field:
        query["academic_field"] = academic_field
    if company_type:
        query["company_type"] = company_type

    personas = await Persona.find(query).to_list()
    return [persona.lead_id for persona in personas]

# Mock function to get email data
async def get_lead_email_by_id(lead_id: str) -> Optional[str]:
    lead = await Lead.find_one(Lead.id == lead_id, projection={"email": 1})
    return lead.email if lead else None

# Utility function to save data to JSON file
def save_to_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Endpoint to save persona details of a lead by lead_id to a JSON file
@app.get("/persona/{lead_id}/save", response_model=Persona)
async def save_persona_by_lead_id_to_json(lead_id: str):
    # Fetch the persona document from the database
    persona = await Persona.find_one(Persona.lead_id == lead_id)
    if persona:
        persona_dict = persona.dict()
        file_name = f"{lead_id}_persona.json"
        save_to_json(persona_dict, file_name)
        return {"message": f"Persona saved to {file_name}"}
    raise HTTPException(status_code=404, detail="Persona not found")

# Lifespan context manager to handle startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app.router.lifespan_context = lifespan


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
