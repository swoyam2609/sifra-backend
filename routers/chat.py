from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from model import message
from dependencies import pass_jwt, mongo, model
from datetime import datetime
import asyncio

router = APIRouter()


@router.post("/chat", tags=["Chat"])
async def chat(message: message.Message, username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user:
        conversation = mongo.db.conversation.find_one({"username": username})
        if conversation:
            chats = mongo.db.chats.find_one({"username": username})
            chats = chats["chat"]
            chats.append(
                {
                    "userType": 0,
                    "time": datetime.utcnow(),
                    'message': message.data
                }
            )
            prevContext = conversation["conversation"]
            currentChats = []
            for i in chats:
                if i["userType"]==0:
                    currentChats.append(f"ME: {i['message']}")
                else:
                    currentChats.append(f"SIFRA: {i['message']}")
            response = model.resumeConversation(prevContext, message.data, currentChats)
            context = model.makeContext(message.data, response, prevContext)
            mongo.db.conversation.update_one({"username": username}, {
                                             "$set": {"conversation": context}})
            chats.append(
                {
                    "userType": 1,
                    "time": datetime.utcnow(),
                    'message': response
                }
            )
            mongo.db.chats.update_one({"username": username}, {
                "$set": {"chat": chats}})
            return JSONResponse(content={"response": response}, status_code=200)
        else:
            messages = [
                {
                    "userType": 0,
                    "time": datetime.utcnow(),
                    'message': message.data
                }
            ]
            response = model.startConversation(message.data)
            context = model.makeContext(message.data, response)
            mongo.db.conversation.insert_one(
                {"username": username, "conversation": context})
            messages.append(
                {
                    "userType": 1,
                    "time": datetime.utcnow(),
                    'message': response
                }
            )
            mongo.db.chats.insert_one({"username": username, "chat": messages})
            return JSONResponse(content={"response": response}, status_code=200)
    else:
        return JSONResponse(content={"error": "Unauthenticated"}, status_code=404)
    
@router.post("/getchats", tags=["Chat"])
def getChats(username: str = Depends(pass_jwt.get_current_user)):
    return StreamingResponse(chatsGenerator(username), media_type="text/event-stream")

async def chatsGenerator(username: str):
    chats = mongo.db.chats.find_one({"username": username})
    if chats:
        messages = chats['chat']
        # messages.sort(reversed=True)
        for message in messages:
            yield str(message)
    else:
        yield None