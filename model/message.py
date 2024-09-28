from pydantic import BaseModel


class Message(BaseModel):
    data: str

class StoryChat(BaseModel):
    story: str
    message: str

class EditStory(BaseModel):
    story: str
    prompt: str