
import datetime
from pydantic import BaseModel


class RequestNotification(BaseModel):
    task_id: int
    task_name: str
    message: str
    user_id: int
    created_at: datetime.datetime


class ResponseNotification(BaseModel):
    id: int
    message: str
    task_name: str
    user_name: str
    created_at: datetime.datetime
    is_read: bool

    class Config:
        from_attributes = True

    