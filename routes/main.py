from http import HTTPStatus
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Response, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from config import get_session
from schemas import mainResponse

from sqlalchemy import select, func
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, status_code=HTTPStatus.OK,)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@router.get('/favicon.ico', status_code=HTTPStatus.OK)
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

@router.post('/hello', response_class=HTMLResponse, status_code=HTTPStatus.OK)
async def hello(request: Request, name: str = Form(...)):
    if name:
        print('Request for hello page received with name=%s' % name)
        return templates.TemplateResponse('hello.html', {"request": request, 'name':name})
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)

@router.get("/info", status_code=HTTPStatus.OK, response_model=mainResponse)
async def info():
    return {
        "message": "FastAPI Example",
        "additional_info": "This is a sample FastAPI application",
        "status": HTTPStatus.OK,
        "data": str(datetime.now(timezone(timedelta(hours=-3))))
    }

@router.get("/mock", status_code=HTTPStatus.TEMPORARY_REDIRECT)
async def mock_endpoint():
    return RedirectResponse(url="/mock/data")

@router.get("/mock/data", status_code=HTTPStatus.OK, response_model=mainResponse)
async def get_mock_data():
    return {"message": "This is mock data", "status": HTTPStatus.OK, "data": str(datetime.now(timezone(timedelta(hours=-3))))}


@router.get("/health", response_model=mainResponse)
def health_check(response: Response, db_conn: Session = Depends(get_session)):
    if db_conn:
        data_from_db_conn = db_conn.execute(select(func.now())).scalar() 
        response.status_code = HTTPStatus.OK
        return {
            "message": "Connected",
            "additional_info": "Database connection established",
            "status": HTTPStatus.OK,
            "data": data_from_db_conn
        }
    else:
        response.status_code = HTTPStatus.BAD_REQUEST
        return {
            "message": "Disconnected",
            "additional_info": "Could not connect to database",
            "status": HTTPStatus.BAD_REQUEST,
            "data": str(datetime.now(timezone(timedelta(hours=-3))))
        }