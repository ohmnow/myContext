from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import PydanticModel
from tortoise.models import Model
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to restrict access to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Person(Model):
    id = fields.IntField(pk=True)
    preferences = fields.JSONField()

    class PydanticMeta:
        exclude = ["id"]

class Person_Pydantic(PydanticModel):
    id: int
    preferences: dict

    class Config:
        orm_mode = True

class PersonIn_Pydantic(PydanticModel):
    preferences: dict

    class Config:
        orm_mode = True

@app.post("/person", response_model=Person_Pydantic, status_code=201)
async def create_person(person: PersonIn_Pydantic):
    """
    Create a new person with the given preferences.

    :param person: The person object containing preferences.
    :return: The created person object.
    """
    obj = await Person.create(**person.dict(exclude_unset=True))
    return await Person_Pydantic.from_tortoise_orm(obj)

@app.get("/person/{person_id}", response_model=Person_Pydantic)
async def get_person(person_id: int):
    """
    Retrieve a person by their ID.

    :param person_id: The unique identifier of the person.
    :return: The person object.
    """
    try:
        return await Person_Pydantic.from_queryset_single(Person.get(id=person_id))
    except Person.DoesNotExist:
        raise HTTPException(status_code=404, detail="Person not found")

@app.put("/person/{person_id}", response_model=Person_Pydantic)
async def update_person(person_id: int, person: PersonIn_Pydantic):
    """
    Update a person's preferences by their ID.

    :param person_id: The unique identifier of the person.
    :param person: The updated person object containing preferences.
    :return: The updated person object.
    """
    await Person.filter(id=person_id).update(**person.dict(exclude_unset=True))
    return await get_person(person_id)

register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL"),
    modules={"models": ["main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)