# для запуска сервера:
# uvicorn main:app --reload
# библиотека имяФайла:переменнаяФастАпи --перезагрузка при сохранении

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import notifications_controller


app = FastAPI(
    title="Notification Service",
    description="Notification Service",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],  # domens/ports
    allow_credentials=True,  # cookie and authorization
    allow_methods=["*"],  # all methods (GET, POST, PUT ...)
    allow_headers=["*"],  # headers in request
)


app.include_router(
    notifications_controller.router, # APIRouter-object
    prefix="/api/notifications", # Prefix for requests
    tags=["Notifications"] # Tags for http://localhost:8000/docs
)
