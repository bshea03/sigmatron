import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.errors import RateLimitExceeded
# from slowapi.middleware import SlowAPIMiddleware
# from slowapi.util import get_remote_address

# from app.database import Base, SessionLocal, engine
# from app.routers.router import api_router
# from app.utils.skill_ranks import normalize_ranks

log = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    # db = SessionLocal()
    
    yield
    
    print("Shutting down...")

app = FastAPI(
    title="My API",
    description="This is a sample API application.",
    version="1.0.0",
)

# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# app.add_middleware(SlowAPIMiddleware)

# CORS setup — allow frontend access
origins = [
    "http://localhost:3000", # frontend hosterd locally
    "https://sigmatron.dev" # your frontend dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(router)

# Health check endpoint
@app.get("/healthchecker")
def health_check():
    return {"message": "Sigmatron API is running"}