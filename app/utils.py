

from datetime import datetime
from models import Notification
from schemas import RequestNotification, ResponseNotification

# Notification to Response Notification
def serilize_notification(notification: Notification) -> ResponseNotification:
    return ResponseNotification(
        id=notification.id,
        message=notification.message,
        task_name=notification.task.name,
        user_name=notification.user.name,
        created_at=notification.created_at,
        is_read=notification.is_read
    )

# Dict to Response Notification
def serilize_jsonToResponseNotification(json: dict) -> ResponseNotification:
    return ResponseNotification(
        id=json.get('id'),
        message=json.get('message'),
        task_name=json.get('task_name'),
        user_name=json.get('user_name'),
        created_at=datetime.fromisoformat(json.get('created_at')),
        is_read=json.get('is_read')
    )


#RequestNotification to Notification
def serilize_requestNotification(request: RequestNotification) -> Notification:
    return Notification(
        message = request.message, 
        task_id = request.task_id,
        user_id = request.user_id,
        is_read = False,
        created_at = request.created_at
    )

#RequestDict to Notification
def serilize_requestDict(request: dict) -> Notification:
    return Notification(
        message = request.get('message'), 
        task_id = request.get('taskId'),
        user_id = request.get('userId'),
        is_read = False,
        created_at = datetime.fromtimestamp(request.get('createdAt')/1000)
    )