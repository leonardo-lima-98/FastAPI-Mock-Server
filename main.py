from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from routes.main import router as default_router
from routes.dashboard import router as dashboard_router
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, adjust as needed
    allow_headers=["*"],  # Allows all headers, adjust as needed
)

app.include_router(default_router, prefix="", tags=["main"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)

