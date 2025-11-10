from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request, 
    current_user = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "tasks": [],
            "teams": []
        }
    )
