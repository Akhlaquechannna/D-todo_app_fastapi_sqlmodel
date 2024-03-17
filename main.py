from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


server = FastAPI()

class Todo (BaseModel):
    id: Optional[int] = None
    name: str 
    description: Optional[str] = None

todos: list [Todo] = []



@server.get("/api/v1/get_todos")
def get_all_todos():
    return todos

@server.post("/api/v1/add_todo")
def add_todo(todo: Todo):
    todos.append(todo)
    return{"message: Todo added succesfully"}


