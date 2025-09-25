from pydantic import BaseModel, Field

class Book(BaseModel):
    title: str = Field(..., max_length=100)
    author: str = Field(..., min_length=1)
    year: int | None = Field(default = None, ge=0, le=2100) 
    price: float | None = None
    