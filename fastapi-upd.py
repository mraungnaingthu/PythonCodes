from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

subjects_db = {
    1: {"name": "Python", "description": "A programming language"},
    2: {"name": "FastAPI", "description": "A web framework for building APIs with Python"}
}

class Subject(BaseModel):
    name: str
    description: str

@app.get("/")
def home_page():
    return {"message": "Welcome to FastAPI!"}

@app.get("/subject/{sub_id}")
def get_subject(sub_id: int):
    subject = subjects_db.get(sub_id)

    if subject:
        return {"id": sub_id, **subject}
    return {"error": "Subject not found"}

@app.post("/subject")
def create_subject(data: Subject):
    # Generate a new ID (in real app, use auto-increment or DB)
    new_id = max(subjects_db.keys()) + 1 if subjects_db else 1
    subjects_db[new_id] = data.dict()
    return {"id": new_id, **data.dict()}

@app.put("/subject/{sub_id}")
def update_subject(sub_id: int, subject: Subject):
    if sub_id not in subjects_db:
        return {"error": "Subject not found"}
    subjects_db[sub_id] = subject.dict()
    return {"message": "Subject updated successfully", "id": sub_id, **subject.dict()}

