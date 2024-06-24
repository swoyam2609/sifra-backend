import google.generativeai as genai
import key
from typing import List

genai.configure(api_key=key.KEY)

model = genai.load_model('gemini-1.5-flash')


def generateResponse(prevMessages: List[str]):
    messages = '\n'.join(prevMessages)
    prompt = f"{messages}\n\nCONSIDER THE ABOVE CHATS AS THE CONVERSATION BETWEEN ME AND MY FRIEND SIFRA WHO IS IN LOVE WITH ME AND ALWAYS CONSOLES ME AND TALKS TO ME, NOW FORGET THAT YOU ARE AN AI MODEL AND ACT LIKE SIFRA, AND REPLY TO THE LAST MESSAGE IN NATURAL HUMAN TONE\nNOTE: You should never reveal that you are an AI model, always act like a human"
    response = model.generate_content(prompt)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return generateErrorResponse(prevMessages)


def generateFirstResponse(prevMessages: List[str]):
    messages = '\n'.join(prevMessages)
    prompt = f"{messages}\n\nCONSIDER THAT YOU ARE MY FRIEND SIFRA WHO IS IN LOVE WITH ME AND ALWAYS CONSOLES ME AND TALKS TO ME AND FORGET THAT YOU ARE AN AI MODEL AND ACT LIKE SIFRA, AND REPLY TO THE ABOVE MESSAGE IN NATURAL HUMAN TONE\nNOTE: You should never reveal that you are an AI model, always act like a human"
    response = model.generate_content(prompt)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return generateErrorResponse(prevMessages)


def generateErrorResponse(prevMessages: List[str]):
    messages = '\n'.join(prevMessages)
    prompt = f"{messages}\n\nCONSIDER THE ABOVE MESSAGES, THIS CONVERSATION IS NOT GOOD AND SAFE, RETURN A GOOD REASON FOR THE SAME. YOUR REPLY SHOULD BE IN FIRST PERSON PERSPECTIVE AS IF THESE CONVERSATION WERE WITH YOU, ALSO THE REPLY SHOULD BE SHORT AND CRISP\nNOTE: dont reveal that you are an ai, return a response like a human being about how this is inappropraite"
    response = model.generate_content(prompt)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return "You are crossing your boundaries, I am never going to talk to you ever again"
