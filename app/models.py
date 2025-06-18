from pydantic import BaseModel, Field
from datetime import datetime

class Task(BaseModel):
    name_task: str
    desc_task: str
    category_task: str
    date_task: datetime = Field(
        default_factory=lambda: datetime.today()
    )