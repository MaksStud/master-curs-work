import uvicorn

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from contextlib import asynccontextmanager

from core.redis import pool
from core.config import settings
from core.constantes import DOCUMENTATION_PAGE

from api.urls import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await pool.disconnect()

app = FastAPI(title=settings.project_name)
app.include_router(router)


@app.get('/')
def redirect_to_docs() -> RedirectResponse:
    """Redirect user from main page to documentation."""
    return RedirectResponse(DOCUMENTATION_PAGE, status_code=status.HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        reload=settings.debug, 
        port=settings.port
        )