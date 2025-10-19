from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from bson import ObjectId
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import List, Optional, Any

load_dotenv()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")


# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database("todo_db")
collection = db.get_collection("todos")

# Pydantic v2 compatible ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        from pydantic_core import core_schema

        def validate(v):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid objectid")
            return ObjectId(v)

        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.no_info_plain_validator_function(validate),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )


class Todo(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: str
    completed: bool = False

    model_config = {
        "arbitrary_types_allowed": True
    }

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo):
    todo_dict = todo.model_dump(by_alias=True, exclude=["id"])
    result = collection.insert_one(todo_dict)
    created_todo = collection.find_one({"_id": result.inserted_id})
    return created_todo

@app.get("/todos/", response_model=List[Todo])
def read_todos():
    todos = []
    for todo in collection.find():
        todos.append(Todo(**todo))
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: str):
    todo = collection.find_one({"_id": ObjectId(todo_id)})
    if todo:
        return Todo(**todo)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, todo: Todo):
    todo_dict = todo.model_dump(by_alias=True, exclude=["id"])
    result = collection.update_one({"_id": ObjectId(todo_id)}, {"$set": todo_dict})
    if result.modified_count == 1:
        updated_todo = collection.find_one({"_id": ObjectId(todo_id)})
        return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    result = collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 1:
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
