from fastapi import FastAPI
from app.routers import users, projects , tasks

app = FastAPI()


app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def home():
    return {"message": "Task Management API"}