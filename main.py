from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import user, chat, sifraextended

app = FastAPI()

app.include_router(user.router)
app.include_router(chat.router)
app.include_router(sifraextended.router)

origins = [
    "https://sifra-prerelease.netlify.app",  
    "https://sifra.swoyam.in", 
    "http://localhost",                     
    "http://localhost:5173",                 
    "http://127.0.0.1",                      
    "http://127.0.0.1:5173",
    "https://sifra.tfugbbsr.in"
]

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
