from fastapi import FastAPI
# from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
from sqlmodel import create_engine, SQLModel, Session, Field, select
from contextlib import asynccontextmanager



load_dotenv()




class Todo (SQLModel,table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    name: str 
    description: Optional[str] = None
print(os.environ.get("DATABASE_URL"))
connection_string = str(os.environ.get("DATABASE_URL")).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
# The first part of the function, before the yield, will
# be executed before the application starts
@asynccontextmanager
async def lifespan(server: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield

server = FastAPI(lifespan = lifespan)


# print(connection_string)
# todos: list [Todo] = []



@server.get("/api/v1/get_todos")
def get_all_todos():
    with Session(engine) as session:
     statement = select(Todo)
     todos = session.exec(statement).all()
     print(todos)
     return todos

@server.post("/api/v1/add_todo")
def add_todo(todo: Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)

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