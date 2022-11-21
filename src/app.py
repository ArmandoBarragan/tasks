from fastapi import FastAPI

from src.routes.timer import router as timer_router
from src.routes.tasks import router as tasks_router
from src.routes.projects import router as projects_router


app = FastAPI()

app.include_router(timer_router)
app.include_router(tasks_router)
app.include_router(projects_router)