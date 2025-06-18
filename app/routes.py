from fastapi import HTTPException
from bson import ObjectId
from typing import List
from fastapi import APIRouter
from app.database import collection
from app.models import Task

router = APIRouter()

@router.get("/")
def read_task():
    tasks = collection.find_one()
    return {"tasks": str(tasks)}

@router.get("/tasks/{category_task}", response_model=List[Task])
def get_tasks_by_category(category_task: str):
    task_cursor = collection.find(
        {"category_task": category_task},
        {"_id": 1, "name_task": 1, "desc_task": 1, "category_task": 1, "date_task": 1}
    )
    tasks = [
        {
            "id": str(task["_id"]),
            "name_task": task.get("name_task"),
            "desc_task": task.get("desc_task"),
            "category_task": task.get("category_task"),
            "date_task": task.get("date_task")
        }
        for task in task_cursor
    ]
    return tasks
    
@router.post("/tasks")
def create_task(task: Task):
    result = collection.insert_one(task.dict())
    return {"id": str(result.inserted_id)}

@router.put("/tasks/{task_id}")
def update_task(task_id: str, task: Task):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="ID inválido.")
    
    obj_id = ObjectId(task_id)
    update_data = {"$set": task.dict()}
    result = collection.update_one({"_id": obj_id}, update_data)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    
    return {"message": "Tarefa atualizada com sucesso"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, task: Task):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="ID inválido.")
    
    result = collection.delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    
    return {"message": "Tarefa deletada com sucesso"}