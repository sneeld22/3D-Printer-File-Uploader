from fastapi import FastAPI
from app.api.v1 import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="3D Print Portal", version="1.0.0")

# Add CORS middleware
origins = [
    "http://localhost:3000",  # your frontend URL, add more if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # allow all headers
)

app.include_router(api_router, prefix="/api/v1")
