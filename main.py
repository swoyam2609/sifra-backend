import speech_recognition as sr
import key
from dependencies import speech
from model import message
from routers import user, chat
import asyncio
import json


recognizer = sr.Recognizer()

token = asyncio.run(user.login_user(key.USERNAME, key.PASSWORD))
token = token['token']
print(token)

while True:
    with sr.Microphone() as source:
        print("Listening :")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            speech.printUser(text)
            if 'jarvis' in text.lower():
                msg = message.Message(data=text)
                response = asyncio.run(chat.chat(msg, master=key.USERNAME, username=token))
                response = response.body.decode()
                response = json.loads(response)
                response = response['response']
                speech.speak(response)
            elif 'shutdown' in text:
                speech.speak('Shutting down')
                break
        except Exception as e:
            print("Error : {}".format(e))