from pydantic import BaseModel


class Album(BaseModel):
    id: int
    title: str
    year: int
    description: str
    price: int
    picture_path: str