from pydantic import BaseModel


class Message(BaseModel):
    data: str

class StoryChat(BaseModel):
    story: str
    message: str