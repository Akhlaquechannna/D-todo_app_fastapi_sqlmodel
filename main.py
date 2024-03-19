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

@server.delete("/api/v1/delete_todo/{id}")
def delete_todo(id: int):
    for i,todo in enumerate(todos):
        # todos[i].id ## another method to go to certain index
        if todo.id == id:
            todos.pop(i)
            print(f'{i} checking index')
    return{f"message: {id} has been successfully deleted"}

@server.patch("/api/v1/update_todo/{id}")
def update_todo(id: int,data:Todo):
    for i, todo in enumerate(todos):
        if todo.id == id:
            todos[i]= data
        else:
            return{f"message: {id} not found"}
    return{f"message: {id} has been successfully updated"}
    
                
    # todos.pop(id)
    # return{f"message: {id} has been delete"}