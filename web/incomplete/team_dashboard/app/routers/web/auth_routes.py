from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.services import user_service as UserService
from app.schemas.user_schema import UserCreate
from app.core.auth import create_access_token
from app.models.user_model import User
from app.schemas.user_schema import PasswordChange
from app.services.user_service import change_user_password


router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not user.verify_password(password):
            return templates.TemplateResponse(
                "auth/login.html",
                {
                    "request": request,
                    "error": "Invalid email or password"
                }
            )
        
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )
        
        response = RedirectResponse(url="/profile", status_code=302)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=3600,
            secure=False,
            samesite="lax"
        )
        
        return response
 

    except Exception as e:
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "error": f"Login failed: {str(e)}"
            }
        )

@router.post("/register")
async def register_submit(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if password != confirm_password:
            return templates.TemplateResponse(
                "auth/register.html",
                {
                    "request": request,
                    "error": "Passwords do not match"
                }
            )
        
        user_data = UserCreate(
            username=username,
            email=email,
            password=password
        )
        
        user = UserService.create_user(db, user_data)
        
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )
        
        response = RedirectResponse(url="/profile", status_code=302)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=3600,
            secure=False,
            samesite="lax"
        )
        
        return response
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": e.detail
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": f"Registration failed: {str(e)}"
            }
        )


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response


@router.get("/profile/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request):
    return templates.TemplateResponse("auth/change-password.html", {"request": request})


@router.post("/profile/change-password")
async def change_password_submit(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Verify passwords match
        if new_password != confirm_password:
            return templates.TemplateResponse(
                "auth/change-password.html",
                {
                    "request": request,
                    "error": "New passwords do not match"
                }
            )
        
        # Verify password strength
        if len(new_password) < 8:
            return templates.TemplateResponse(
                "auth/change-password.html",
                {
                    "request": request,
                    "error": "New password must be at least 8 characters long"
                }
            )
        
        # Create password change data
        password_data = PasswordChange(
            current_password=current_password,
            new_password=new_password
        )
        
        # Update password using service
        updated_user = change_user_password(db, current_user.id, password_data)
        
        # Redirect to profile with success message
        response = RedirectResponse(url="/profile", status_code=302)
        return response
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "auth/change-password.html",
            {
                "request": request,
                "error": e.detail
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "auth/change-password.html",
            {
                "request": request,
                "error": f"Password change failed: {str(e)}"
            }
        )
