from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from model import Person   # or wherever your Person class lives

app = FastAPI(title="People Normalization API")
#Request structure for API
class NormalizeRequest(BaseModel):
    people: List[Dict]
#Response structure for API
class NormalizeResponse(BaseModel):
    valid_people: List[Person]
    errors: List[str]
#App controller
@app.post("/normalize", response_model=NormalizeResponse)
def normalize_people_api(payload: NormalizeRequest):
    valid_people = []
    errors = []

    for record in payload.people:
        try:
            person = Person(**record)
            valid_people.append(person)
        except ValidationError as e:
            errors.append(f"{record} → {e.errors()}")

    return NormalizeResponse(
        valid_people=valid_people,
        errors=errors
    )