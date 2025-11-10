from fastapi import APIRouter
from .auth_routes import router as auth_router
from .page_routes import router as page_router
from .profile_routes import router as profile_router
from .dashboard_routes import router as dashboard_router
from .task_routes import router as task_router
from .team_routes import router as team_router

# Create main web router
router = APIRouter()

# Include all web routers
router.include_router(auth_router)
router.include_router(page_router)
router.include_router(profile_router)
router.include_router(dashboard_router)
router.include_router(task_router)
router.include_router(team_router)
