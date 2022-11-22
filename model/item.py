from pydantic import BaseModel, Field


class Item(BaseModel):
    # id: str = Field(default=None)
    pid: str = Field(default=None)
    name: str = Field(default=None)
    price: str = Field(default=None)
    rating: str = Field(default=None)
    sales: str = Field(default=None)
    review: str = Field(default=None)
    img: str = Field(default=None)
    url: str = Field(default=None)


class TrackItem(BaseModel):
    token: str = Field(default=None)
    pid: str = Field(default=None)
