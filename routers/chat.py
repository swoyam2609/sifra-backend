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
            conversation["conversation"].append(f"{user["name"]}: {message.data}")
            mongo.db.conversation.update_one({"username": username}, {"$set": {"conversation": conversation["conversation"]}})
            response = model.generateResponse(conversation["conversation"])
            conversation["conversation"].append(f"sifra: {response}")
            mongo.db.conversation.update_one({"username": username}, {"$set": {"conversation": conversation["conversation"]}})
            return JSONResponse(content={"response": response}, status_code=200)
        else:
            data = [message.data]
            mongo.db.conversation.update_one({"username": username}, {"$set": {"conversation": data}})
            response = model.generateFirstResponse(data)
            data.append(response)
            mongo.db.conversation.insert_one({"username": username, "conversation": data})
            return JSONResponse(content={"response": response}, status_code=200)
    else:
        return JSONResponse(content={"error": "Unauthenticated"}, status_code=404)