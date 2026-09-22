from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, projects, tasks


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "Task Management API"}