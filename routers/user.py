from fastapi import APIRouter, Depends
from model import user
from dependencies import mongo, email_auth, pass_jwt
from fastapi.responses import JSONResponse

router = APIRouter()


async def signup(user: user.User):
    newuser = {
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "password": pass_jwt.create_hashed_password(user.password)
    }
    mongo.db.users.insert_one(newuser)
    return {"message": "User created successfully"}


@router.post("/users/signup", tags=["User"])
async def signup_user(user: user.User):
    if mongo.db.users.find_one({"email": user.email}):
        return JSONResponse(content={"message": "Email already exists"}, status_code=400)
    elif mongo.db.users.find_one({"username": user.username}):
        return JSONResponse(content={"message": "Username already exists"}, status_code=400)
    else:
        email_auth.send_otp(user.email)
        return JSONResponse(content={"message": "OTP sent successfully"}, status_code=200)


@router.post("/users/signup/verify", tags=["User"])
async def verify_user(user: user.User, otp: str):
    response = email_auth.verify_otp(user.email, otp)
    if response == True:
        return await signup(user)
    else:
        return response


@router.get("/users/login", tags=["User"])
async def login_user(username: str, password: str):
    user = mongo.db.users.find_one({"username": username})
    if user:
        if pass_jwt.verify_password(password, user["password"]):
            jwt_token = pass_jwt.create_jwt_token(
                {"username": user["username"]})
            return {"message": "Login successful", "token": jwt_token, "token_type": "bearer"}
        else:
            return JSONResponse(content={"message": "Password is incorrect"}, status_code=400)
    else:
        return JSONResponse(content={"message": "Username not found"}, status_code=400)


@router.delete("/users/delete", tags=["User"])
async def delete_user(username: str):
    user = mongo.db.users.find_one({"username": username})
    if user:
        email_auth.send_otp(user["email"])
        return JSONResponse(content={"message": "OTP sent successfully"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Username not found"}, status_code=400)


@router.delete("/users/delete/verify", tags=["User"])
async def verify_delete_user(username: str, otp: str):
    user = mongo.db.users.find_one({"username": username})
    response = email_auth.verify_otp(user["email"], otp)
    if response == True:
        mongo.db.users.delete_one({"username": username})
        return {"message": "User deleted successfully"}
    else:
        return response


@router.get("/user", tags=["User"])
async def getUser(username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user:
        content = {
            "username":user["username"],
            "email": user["email"],
            "name": user["name"],
        }
        return JSONResponse(content=content, status_code=200)
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)
    
@router.post("/user/waitlist", tags=["User"])
async def add_to_waitlist(email: str):
    if mongo.db.waitlist.find_one({"email": email}):
        return JSONResponse(content={"message": "Email already exists in waitlist"}, status_code=400)
    else:
        mongo.db.waitlist.insert_one({"email": email})
        return JSONResponse(content={"message": "Email added to waitlist successfully"}, status_code=201)
    
@router.post("/user/forgetpassword", tags=["User"])
async def forget_password(email: str):
    user = mongo.db.users.find_one({"email": email})
    username = mongo.db.users.find_one({"username":email})
    if user:
        email_auth.send_otp(email)
        return JSONResponse(content={"message": "OTP sent successfully"}, status_code=200)
    elif username:
        email_auth.send_otp(username["email"])
        return JSONResponse(content={"message": "OTP sent successfully"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Email/Username not found"}, status_code=404)
    

@router.post("/user/forgetpassword/verify", tags=["User"])
async def verify_forget_password(email: str, otp: str, new_password: str):
    user = mongo.db.users.find_one({"email": email})
    username = mongo.db.users.find_one({"username":email})
    if user:
        response = email_auth.verify_otp(email, otp)
        if response == True:
            mongo.db.users.update_one({"email": email}, {"$set": {"password": pass_jwt.create_hashed_password(new_password)}})
            return JSONResponse(content={"message": "Password updated successfully"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Incorrect OTP"}, status_code=404)
    elif username:
        response = email_auth.verify_otp(username["email"], otp)
        if response == True:
            mongo.db.users.update_one({"username": username["username"]}, {"$set": {"password":pass_jwt.create_hashed_password(new_password)}})
            return JSONResponse(content={"message": "Password updated successfully"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Incorrect OTP"}, status_code=404)