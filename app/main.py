from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.route import router

app = FastAPI()

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, adjust as needed
    allow_headers=["*"],  # Allows all headers, adjust as needed
)

app.include_router(router)
