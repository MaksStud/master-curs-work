from fastapi import FastAPI
import uvicorn
from core.config import settings

app = FastAPI(title=settings.project_name)



if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        reload=settings.debug, 
        port=settings.port
        )