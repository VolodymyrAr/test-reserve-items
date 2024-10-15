from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int = 10
    offset: int = 0


class ID(BaseModel):
    id: int


class Action(BaseModel):
    success: bool = True
    message: str
