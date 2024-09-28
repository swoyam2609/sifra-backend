from fastapi import APIRouter
from model import message
from fastapi.responses import JSONResponse
from dependencies import model

router = APIRouter()

@router.post("/sifra-extended/chat", tags=["Sifra-Extended"])
async def sifra_extended_chat(data: message.StoryChat):
    try:
        response = model.chatWithStory(data.story, data.message)
        return JSONResponse(content={"response": response}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.post("/sifra-extended/edit-story", tags=["Sifra-Extended"])
async def sifra_extended_(data: message.EditStory):
    try:
        response = model.editStory(data.story, data.prompt)
        return JSONResponse(content={"response": response}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)