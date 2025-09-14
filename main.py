from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    duck = "duck"
    dog = "dog"
    cat = "cat"


fake_items_db = [{"item_name": "Apple"}, {"item_name": "Pear"}, {"item_name": "Orange"}]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

# order of path operations matters
@app.get("/users/me")
async def read_user_me():
    return {"user_id" :"the current user"}

#Path Parameters with types
@app.get("users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# Path Parameters with Enums                    
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.duck:
        return {"model_name": model_name, "message": "Quack quack model!"}
    
    if model_name.value =="dog":
        return {"model_name": model_name, "message": "Woof woof model!"}
    
    return {"model_name": model_name, "message": "Meow meow model!"}

# Path Query Parameters (naturally strings, but can have data conversion with Python types)
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]

# Optional Query Parameters and Type Conversion
@app.get("/items/{item_id}")
async def read_item(item_id: str, q:str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a loooooonnng description"}
        )
    return item


# Multiple path and query parameters (required and not requireds)
@app.get("users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a loooooonnng description again"}
        )
        return item