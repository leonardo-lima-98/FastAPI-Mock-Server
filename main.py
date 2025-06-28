import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from routes.main import router as default_router
from routes.dashboard import router as dashboard_router
from routes.stats import router as stats_router

from starlette.exceptions import HTTPException as StarletteHTTPException


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
app.include_router(stats_router, prefix="/stats", tags=["stats"])


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)

