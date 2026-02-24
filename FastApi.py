from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Welcome to FastAPI!"}

@app.get("/subject/{subject_id}")
def get_subject(subject_id: int):
    subjects = {
        1: "Python Programming",
        2: "Java Programming",
        3: "C Programming"
    }
    return {"subject": subjects.get(subject_id, "Subject not found")}