from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserUpdate
from app.services.user_service import update_user


router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request, 
    current_user = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "user/profile.html",
        {
            "request": request,
            "user": current_user,
            "tasks": [],
            "teams": [],
            "completed_tasks": [],
            "recent_activity": []
        }
    )


@router.get("/profile/edit", response_class=HTMLResponse)
async def edit_profile_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "user/edit-profile.html", 
        {
            "request": request,
            "user": current_user
        }
    )


@router.post("/profile/edit")
async def edit_profile_submit(
    request: Request,
    username: str = Form(None),
    email: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Create update data (only include provided fields)
        update_data = {}
        if username and username != current_user.username:
            update_data["username"] = username
        if email and email != current_user.email:
            update_data["email"] = email
        
        # If no changes were made, redirect back
        if not update_data:
            return RedirectResponse(url="/profile", status_code=302)
        
        # Create UserUpdate schema
        user_update = UserUpdate(**update_data)
        
        # Update user
        updated_user = update_user(db, current_user.id, user_update)
        
        # Redirect to profile with success
        response = RedirectResponse(url="/profile", status_code=302)
        return response
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "user/edit-profile.html",
            {
                "request": request,
                "user": current_user,
                "error": e.detail
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "user/edit-profile.html",
            {
                "request": request,
                "user": current_user,
                "error": f"Profile update failed: {str(e)}"
            }
        )
