from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from model import message
from dependencies import pass_jwt, mongo, model

router = APIRouter()


@router.post("/chat", tags=["Chat"])
async def chat(message: message.Message, username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user:
        conversation = mongo.db.conversation.find_one({"username": username})
        if conversation:
            prevContext = conversation["conversation"]
            response = model.resumeConversation(prevContext, message.data)
            context = model.makeContext(message.data, response, prevContext)
            mongo.db.conversation.update_one({"username": username}, {"$set": {"conversation": context}})
            return JSONResponse(content={"response": response}, status_code=200)
        else:
            response = model.startConversation(message.data)
            context = model.makeContext(message.data, response)
            mongo.db.conversation.insert_one({"username": username, "conversation": context})
            return JSONResponse(content={"response": response}, status_code=200)
    else:
        return JSONResponse(content={"error": "Unauthenticated"}, status_code=404)