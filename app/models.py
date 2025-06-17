from pydantic import BaseModel

class Task(BaseModel):
    name_task: str
    desc_task: str