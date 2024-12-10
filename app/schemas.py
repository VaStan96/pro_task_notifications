
import datetime
from pydantic import BaseModel


class RequestNotification(BaseModel):
    message: str
    task_id: int
    user_id: int


class ResponseNotification(BaseModel):
    id: int
    message: str
    task_name: str
    user_name: str
    created_at: datetime.datetime
    is_read: bool

    class Config:
        orm_mode = True

    