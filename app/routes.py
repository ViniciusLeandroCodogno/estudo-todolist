from fastapi import HTTPException
from bson import ObjectId
from fastapi import APIRouter
from app.database import collection
from app.models import Task

router = APIRouter()

@router.get("/")
def read_task():
    tasks = collection.find_one()
    return {"tasks": str(tasks)}

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