from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import user, chat

app = FastAPI()

app.include_router(user.router)
app.include_router(chat.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"author" : "Swoyam"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)