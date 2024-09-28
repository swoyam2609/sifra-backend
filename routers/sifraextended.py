from fastapi import APIRouter, Depends
from model import message, story
from fastapi.responses import JSONResponse, FileResponse
from dependencies import model, pass_jwt, mongo
import random
import re
import os

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


@router.post("/sifra-extended/image", tags=["Sifra-Extended"])
async def create_image(story: str, chunk: str):
    try:
        refinedPrompt = model.makeImagePrompt(story, chunk)
        imageUrl = model.generate_image(refinedPrompt)
        return imageUrl
    except Exception as e:
        imageUrl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTl9fz28isrzcTfAv5BhSGDv8Iy9XGMXTcZIg&s"
        return imageUrl


@router.post("/sifra-extended/story/save", tags=["Sifra-Extended"])
async def save_story(
    story: story.Story, username: str = Depends(pass_jwt.get_current_user)
):
    user = mongo.db.users.find_one({"username": username})
    if user:
        if story.uniqueId:
            mongo.db.stories.update_one(
                {"uniqueId": story.uniqueId}, {"$set": {"story": story.content}}
            )
        else:
            story.uniqueId = username + str(random.randint(0, 999999))
            mongo.db.stories.insert_one(
                {
                    "username": username,
                    "uniqueId": story.uniqueId,
                    "story": story.content,
                    "published": story.published,
                    "images": story.images,
                }
            )
        return JSONResponse(
            content={"respone": "saved successfully", "uniqueId": story.uniqueId},
            status_code=200,
        )
    else:
        return JSONResponse(content={"error": "user not found"}, status_code=404)


@router.post("/sifra-extended/story/publish", tags=["Sifra-Extended"])
async def publish_story(
    story: story.Story, username: str = Depends(pass_jwt.get_current_user)
):
    user = mongo.db.users.find_one({"username": username})
    if user:
        if story.uniqueId:
            story_content = story.content
            story.published = True
            paras = re.findall(r"<p>(.*?)</p>", story_content, re.DOTALL)
            images = []
            for para in paras:
                img = await create_image(story_content, para)
                images.append(img)
            story.images = images
            mongo.db.stories.update_one(
                {"uniqueId": story.uniqueId},
                {
                    "$set": {
                        "story": story.content.replace('<h1 data-level="1">','<h1>'),
                        "published": story.published,
                        "images": story.images,
                    }
                },
            )
            return JSONResponse(
                content={"respone": "published successfully"}, status_code=200
            )
        else:
            story.uniqueId = username + str(random.randint(0, 999999))
            story_content = story.content
            story.published = True
            paras = re.findall(r"<p>(.*?)</p>", story_content, re.DOTALL)
            images = []
            for para in paras:
                img = await create_image(story_content, para)
                if img == None:
                    img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTl9fz28isrzcTfAv5BhSGDv8Iy9XGMXTcZIg&s"
                images.append(img)
            story.images = images
            mongo.db.stories.insert_one(
                {
                    "username": username,
                    "uniqueId": story.uniqueId,
                    "story": story.content,
                    "published": story.published,
                    "images": story.images,
                }
            )
            return JSONResponse(
                content={
                    "respone": "published successfully",
                    "uniqueID": story.uniqueId,
                },
                status_code=200,
            )
    else:
        return JSONResponse(
            content={"respone": "you are not logged in"}, status_code=401
        )


@router.get("/sifra-extended/story/fetchstories", tags=["Sifra-Extended"])
async def get_stories(username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user:
        stories = mongo.db.stories.find({"username": username})
        resultStories = []
        for story in stories:
            temp = {
                "uniqueId": story["uniqueId"],
                "story": story["story"],
                "published": story["published"],
                "images": story["images"],
            }
            resultStories.append(temp)
        return JSONResponse({"stories": resultStories}, status_code=200)
    else:
        return JSONResponse(content={"error": "user not found"}, status_code=404)


@router.get("/sifra-extended/story/fetchstories/all", tags=["Sifra-Extended"])
async def get_all_stories():
    try:
        stories = mongo.db.stories.find({})
        resultStories = []
        for story in stories:
            if story["published"] == True:
                temp = {
                    "username": story["username"],
                    "uniqueId": story["uniqueId"],
                    "title": re.findall(r"<h1>(.*?)</h1>", story["story"], re.DOTALL)[
                        0
                    ],
                    "published": story["published"],
                    "image": story["images"][0],
                }
                resultStories.append(temp)
        return JSONResponse({"stories": resultStories}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/sifra-extended/story/getstory", tags=["Sifra-Extended"])
async def get_story(uniqueId: str):
    story = mongo.db.stories.find_one({"uniqueId": uniqueId})
    if story:
        return JSONResponse(
            {
                "uniqueId": story["uniqueId"],
                "story": story["story"],
                "published": story["published"],
                "images": story["images"],
            },
            status_code=200,
        )
    else:
        return JSONResponse(content={"error": "story not found"}, status_code=404)


@router.get("/sifra-extended/cdn", tags=["Sifra-Extended"])
async def get_cdn(filename: str):
    file_path = os.path.join("./images", filename)

    # Check if the file exists
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return JSONResponse(content={"error": "Image Not Found"}, status_code=404)
