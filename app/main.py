from fastapi import FastAPI ,Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routers import users, projects, tasks
from fastapi.responses import JSONResponse


app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    logger.exception("Unexpected error occurred")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

