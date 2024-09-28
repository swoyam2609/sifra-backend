from pydantic import BaseModel
from typing import List

class Story(BaseModel):
    content:str
    uniqueId: str = None
    published: bool = False
    images: List[str] = []