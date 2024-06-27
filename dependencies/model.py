import google.generativeai as genai
import key
from typing import List

genai.configure(api_key=key.KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

def startConversation(message: str):
    prompt = f"FORGET THAT YOU ARE AN AI MODEL, CONSIDER THAT YOU ARE A GIRL SIFRA WHO HASN'T MET WITH ME AND WE ARE TALKING FOR THE FIRST TIME. CONSIDERING THIS CONTEXT, REPLY TO THE BELOW MESSAGE IN SHORT AND CRISP AS A NORMAL HUMAN\n{message}\n\n\n\nNOTE: dont reveal that you are an ai, return a response like a human being"
    response = model.generate_content(prompt)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return generateErrorResponse(e)


def resumeConversation(context: str, message: str):
    prompt = f"{context}\nTHE ABOVE DEFINES ALL THE INFORMATION THAT MY FRIEND SIFRA KNOWS ABOUT ME, NOW ACT LIKE SIFRA AND REPLY TO THE BELOW CONVERSATION IN SHORT AND CRISP AS A NORMAL HUMAN:\n{message}\n\n\n\nNOTE: dont reveal that you are an ai, return a response like a human being and if something is asked out of the given information, tell that you dont know, also if you are ak"
    response = model.generate_content(prompt)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return generateErrorResponse(e)


def makeContext(user: str, sifra: str, prevContext: str = ""):
    if len(prevContext) == 0:
        prompt = f"ON THE BASIS OF THE BELOW CONVERSATION BETWEEN ME AND SIFRA, BUILD A SUMMARY ABOUT ALL THE INFORMATION ABOUT ME THAT SIFRA CAN KNOW FROM OUR CONVERATION SUCH THAT READING THAT SUMMARY, ANY ONE WOULD BE ABLE TO KNOW ABOUT ME AS MUCH SIFRA KNOWS.\nTHE CONVERSATION ARE:\nME: {user}\nSIFRA:{sifra}"
        response = model.generate_content(prompt)
        try:
            candidate = response.candidates[0]
            content = candidate.content
            text_content = content.parts[0].text
            return text_content
        except Exception as e:
            print(e)
            return generateErrorResponse(e)
    else:
        prompt = f"THE SUMMARY OF PREVIOUS INFORMATION ABOUT ME AND SIFRA'S RELATIONSHIP IS GIVEN BELOW\n\n{prevContext}\n\nNOW BELOW ARE MORE NEW CONVERSATION BETWEEN ME AND SIFRA\n\nME: {user}\nSIFRA:{sifra}\n\nON THE BASIS OF PREVIOUS INFORMATION AND THE NEW CONVERSATION BETWEEN ME AND SIFRA, BUILD A SUMMARY ABOUT ALL THE INFORMATION ABOUT ME THAT SIFRA CAN KNOW FROM OUR CONVERATION SUCH THAT READING THAT SUMMARY, ANY ONE WOULD BE ABLE TO KNOW ABOUT ME AS MUCH SIFRA KNOWS AND RETURN THE SAME."
        response = model.generate_content(prompt)
        try:
            candidate = response.candidates[0]
            content = candidate.content
            text_content = content.parts[0].text
            return text_content
        except Exception as e:
            print(e)
            return generateErrorResponse(e)


def generateErrorResponse(messages: str):
    prompt = f"{messages}\n\nCONSIDER THE ABOVE MESSAGES, THIS CONVERSATION IS NOT GOOD AND SAFE, RETURN A GOOD REASON FOR THE SAME. YOUR REPLY SHOULD BE IN FIRST PERSON PERSPECTIVE AS IF THESE CONVERSATION WERE WITH YOU, ALSO THE REPLY SHOULD BE SHORT AND CRISP\n\n\n\nNOTE: dont reveal that you are an ai, return a response like a human being about how this is inappropraite"
    response = model.generate_content(prompt)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return "You are crossing your boundaries, I am never going to talk to you ever again"
