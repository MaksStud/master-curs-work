from fastapi import APIRouter
from api.users import router as users_router


router = APIRouter(prefix='/api')

router.include_router(users_router)
