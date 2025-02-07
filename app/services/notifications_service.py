import json
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import RequestNotification, ResponseNotification
from repositories import notifications_repository, tasks_repository, cache_notifications_repository
import utils

from datetime import datetime, timedelta

async def fetch_notifications(db: AsyncSession):
    # cache
    cached_notifications = await cache_notifications_repository.get_data("all_notifications")
    if cached_notifications:
        # deserialize cache (JSON in Pydantic)
        response_notifications_list = json.loads(cached_notifications)
        response_notifications = [utils.serilize_jsonToResponseNotification(notif) for notif in response_notifications_list]
    else:
        # DB
        db_notifications = await notifications_repository.get_all(db)

        if not db_notifications:
            raise HTTPException(status_code=404, detail="No notifications found")
        # serialize DB (SQL-schema in Pydantic)
        response_notifications = [utils.serilize_notification(notif) for notif in db_notifications]
        # serialize DB (Pydantic in JSON) and save in cache
        await cache_notifications_repository.set_data("all_notifications", json.dumps([{**notif.model_dump(), "created_at": notif.created_at.isoformat()} for notif in response_notifications]))
    
    return response_notifications

async def fetch_notifications_by_user(db: AsyncSession, id: int):
    cached_notifications = await cache_notifications_repository.get_data(f"notificationsByUser:{id}")

    if cached_notifications:
        response_notifications_list = json.loads(cached_notifications)
        response_notifications = [utils.serilize_jsonToResponseNotification(notif) for notif in response_notifications_list]
    else:
        db_notifications = await notifications_repository.get_for_user(db, id)

        if not db_notifications:
            raise HTTPException(status_code=404, detail="No notifications found")
        
        response_notifications = [utils.serilize_notification(notif) for notif in db_notifications]

        await cache_notifications_repository.set_data(f"notificationsByUser:{id}", json.dumps([{**notif.model_dump(), "created_at": notif.created_at.isoformat()} for notif in response_notifications]))
    
    return response_notifications


async def create_new_notification(new_request: dict, db: AsyncSession):
    complett_notification = utils.serilize_requestDict(new_request)
    
    request_notification = await notifications_repository.new(complett_notification, db)
    if request_notification is None:
        raise HTTPException(status_code=404, detail="Failed to create notification")
    
    response = utils.serilize_notification(request_notification)

    # Serialize (Pydantic in JSON) automatiic witn "request_notification.json()"
    await cache_notifications_repository.set_data(f"notificationByID:{complett_notification.id}", response.model_dump()) 
    await cache_notifications_repository.del_data("all_notifications")
    await cache_notifications_repository.del_data(f"notificationsByUser:{complett_notification.user_id}")

    return response


async def reading (id: int, db: AsyncSession):

    notification = await notifications_repository.getByID(id, db)
    if not notification:
            raise HTTPException(status_code=404, detail="No notification with ID {id} found")
    
    notification.is_read = True
    readed_notification = await notifications_repository.saveChanges(notification, db)
    if not readed_notification:
        raise HTTPException(status_code=404, detail="Failed to mark notification")
    
    response = utils.serilize_notification(readed_notification)
    
    await cache_notifications_repository.set_data(f"notificationByID:{id}", response.model_dump())
    await cache_notifications_repository.del_data("all_notifications")
    await cache_notifications_repository.del_data(f"notificationsByUser:{readed_notification.user_id}")
    
    return response


async def check_deadline(db: AsyncSession):
    # --filter here--
    # # get all tasks
    # db_tasks = await tasks_repository.get_all(db)
    # if not db_tasks:
    #     raise HTTPException(status_code=404, detail="No tasks found")

    # ending_tasks = [] 
    # deadline_limit = datetime.now() + timedelta(hours=24)
    
    # # filter by deadline
    # for task in db_tasks:
    #     if task.deadline <= deadline_limit:
    #         ending_tasks.append(task)
    
    # # get all notifications
    # db_notifications = await notifications_repository.get_all(db)
    # if not db_notifications:
    #     raise HTTPException(status_code=404, detail="No notifications found")
    
    # # filter by taskId and message
    # for task in ending_tasks:
    #     for notif in db_notifications:
    #         if notif.task_id == task.id and notif.message.startswith("Attention!"):
    #             ending_tasks.pop(task)
    #             break

    
    # --filter in repositories--
    # get tasks with deadline
    deadline_limit = datetime.now() + timedelta(hours=24)
    ending_tasks = await tasks_repository.get_tasks_with_deadline(db, deadline_limit)
    if not ending_tasks:
         raise HTTPException(status_code=404, detail="No tasks found")
    
    # convert Sequnce to List
    ending_tasks = list(ending_tasks)
    
    # check notifications
    for task in ending_tasks:
        existing_notification = await notifications_repository.get_notification_with_deadline(db, task.id)
        if existing_notification:
            ending_tasks.pop(task)

    # create new notifications
    responces = []
    for task in ending_tasks:
        new_request = {}
        new_request["taskId"] = task.id
        new_request["userId"] = task.userId
        new_request["message"] = "Attention! The deadline for Task " + task.name + " is tomorrow."
        new_request["createdAt"] = int(datetime.now().timestamp()*1000)

        responce = await create_new_notification(new_request, db)
        responces.append(responce)

    return responces
    
    
