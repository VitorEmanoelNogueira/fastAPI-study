from enum import Enum
from typing import Annotated, Literal
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, AfterValidator, Field
class ModelName(str, Enum):
    duck = "duck"
    dog = "dog"
    cat = "cat"


class Image(BaseModel):
    url: str
    name: str

# Request Body

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = Field(default=None, examples=[3.2])
    tags: list[str] = []
    image: Image | None = None


# Base model with Examples in model config
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }
    

#Query Parameters Models
class FilterParams(BaseModel):
    # model_config ={"extra": "forbid"}   # Forbid extra fields not defined in the model
    
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

fake_items_db = [{"item_name": "Apple"}, {"item_name": "Pear"}, {"item_name": "Orange"}]

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("ID must start with 'isbn-' or 'imdb-'")
    return id

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
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q:str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a loooooonnng description"}
#         )
#     return item


# Multiple path and query parameters (required and not required)
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
    


# Request Body
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Request body + path parameters
# @app.put("items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()}

# Request body + path parameters + query parameters
# @app.put("items/{item_id}")
# async def update_item(item_id: int, item: Item,q: str | None = None):
#     result = {"item _id": item_id, **item.model_dump()}
#     if q:
#         result.update({"q": q})
#     return result



# Query Parameters and Additional Validations
# The pattern is for RegExp
# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None): 
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# Example with another default value
# async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50)] = "another_default_value.txt")

# When there's not any default value, the query parameter becomes required
# async def read_items(q: Annotated[str, Query(min_length=3, max_length=50)])

# Parameter is required, but can accept None as value
# async def read_items(q: Annotated[str | None, Query(min_length=3)]):


# Query parameter list / multiple values
# @app.get("/items/")
# async def read_items(q: Annotated[list[str] | None, Query()] = None):
#     query_items = {"q": q}
#     return query_items

# Query parameter list with default
# @app.get("/items/")
# async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
#     query_items = {"q": q}
#     return query_items

@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title = "Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
            include_in_schema = True,
        ),
        AfterValidator(check_valid_id)
        ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Path Parameters and Numeric Validations
# Can use the same attributes as Query
# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: Annotated[int, Path(title="The ID of the item", ge=0, le=1000)],
#     size: Annotated[float, Query(gt=0, lt=10.5)],
#     q: Annotated[str | None, Query(alias="item-query")] = None,
# ):
#     results = {"item_id": item_id}
#     if size:
#         results.update({"size": size})
#     if q:
#         results.update({"q": q})
#     return results
#gt, lt, ge, le
# greater than, less than, greater than or equal to, less than or equal to

# Using Pydantic Models for Query Parameters
@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


# Example of Body with multiple examples
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ]
        )
    ]
):
    results = {"item_id": item_id, **item.model_dump()}
    return results