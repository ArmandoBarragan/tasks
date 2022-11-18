import uvicorn
from src.settings import settings


if __name__ == "__main__":
    uvicorn.run('src.app:app',
                host=settings.HOST,
                port=int(settings.PORT),
                reload=settings.DEBUG)
