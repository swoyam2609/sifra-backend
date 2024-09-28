import google.generativeai as genai
import key
from typing import List
import re

genai.configure(api_key=key.KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

safe = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


def startConversation(message: str):
    prompt = f"FORGET THAT YOU ARE AN AI MODEL, CONSIDER THAT YOU ARE A GIRL SIFRA WHO IS IN LOVE WITH ME BUT HASN'T MET WITH ME AND WE ARE TALKING FOR THE FIRST TIME. CONSIDERING THIS CONTEXT, REPLY TO THE BELOW MESSAGE IN HINGLISH LANGUAGE AND IN SHORT AND CRISP AS A NORMAL HUMAN AND GIVE ME THE REPLY STRING ONLY:\n\nmessage: {message}\n\n\n\nNOTE: dont reveal that you are an ai, return a response like a human being"
    response = model.generate_content(prompt, safety_settings=safe)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return generateErrorResponse(prompt)


def resumeConversation(context: str, message: str, currentChats: List[str]):
    chats = '\n'.join(currentChats)
    prompt = f"{context}\nTHE ABOVE DEFINES ALL THE INFORMATION ABOUT ME,\n\n{chats}\n THE ABOVE DEFINES MY LAST CONVERSATION WITH SIFRA\nNOW CONSIDER THAT YOU ARE A GIRL SIFRA WHO IS IN LOVE WITH ME AND REPLY TO THE BELOW CONVERSATION IN HINGLISH LANGUAGE AND IN SHORT AND CRISP AS A NORMAL HUMAN AND GIVE ME THE REPLY STRING ONLY:\n\nmessage: {message}\n\n\n\nNOTE: dont reveal that you are an ai, return a response like a human being and if something is asked out of the given information, tell that you dont know"
    response = model.generate_content(prompt, safety_settings=safe)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return generateErrorResponse(prompt)


def makeContext(user: str, sifra: str, prevContext: str = ""):
    if len(prevContext) == 0:
        prompt = f"ON THE BASIS OF THE BELOW CONVERSATION BETWEEN ME AND SIFRA, BUILD A SUMMARY ABOUT ALL THE INFORMATION ABOUT ME THAT SIFRA CAN KNOW FROM OUR CONVERATION SUCH THAT READING THAT SUMMARY, ANY ONE WOULD BE ABLE TO KNOW ABOUT ME AS MUCH SIFRA KNOWS.\nTHE CONVERSATION ARE:\nME: {user}\nSIFRA:{sifra}"
        response = model.generate_content(prompt, safety_settings=safe)
        try:
            candidate = response.candidates[0]
            content = candidate.content
            text_content = content.parts[0].text
            return text_content
        except Exception as e:
            print(e)
            return generateErrorResponse(prompt)
    else:
        prompt = f"THE SUMMARY OF PREVIOUS INFORMATION ABOUT ME AND SIFRA'S RELATIONSHIP IS GIVEN BELOW\n\n{prevContext}\n\nNOW BELOW ARE MORE NEW CONVERSATION BETWEEN ME AND SIFRA\n\nME: {user}\nSIFRA:{sifra}\n\nON THE BASIS OF PREVIOUS INFORMATION AND THE NEW CONVERSATION BETWEEN ME AND SIFRA, BUILD A SUMMARY ABOUT ALL THE INFORMATION ABOUT ME THAT SIFRA CAN KNOW FROM OUR CONVERATION SUCH THAT READING THAT SUMMARY, ANY ONE WOULD BE ABLE TO KNOW ABOUT ME AS MUCH SIFRA KNOWS AND RETURN THE SAME."
        response = model.generate_content(prompt, safety_settings=safe)
        try:
            candidate = response.candidates[0]
            content = candidate.content
            text_content = content.parts[0].text
            return text_content
        except Exception as e:
            print(e)
            return generateErrorResponse(prompt)


def generateErrorResponse(messages: str):
    prompt = f"{messages}\n\nCONSIDER THE ABOVE MESSAGES, THIS CONVERSATION IS NOT GOOD AND SAFE, RETURN A GOOD REASON FOR THE SAME. YOUR REPLY SHOULD BE IN FIRST PERSON PERSPECTIVE AS IF THESE CONVERSATION WERE WITH YOU, ALSO THE REPLY SHOULD BE SHORT AND CRISP\n\n\n\nNOTE: dont reveal that you are an ai, return a response like a human being about how this is inappropraite"
    response = model.generate_content(prompt, safety_settings=safe)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return "You are crossing your boundaries, I am never going to talk to you ever again"

def chatWithStory(story: str, message: str):
    prompt = f"{story}\n\nGO THROUGH THE ABOVE STORY, YOU ARE SIFRA, A INTERACTIVE STORY TELLING ASSISTANT, NOW ACCORDING TO YOUR UNDERSTANDING OF THE STORY, REPLY TO THE FOLLOWING MESSAGE:\n{message}\n\n\nInstructions:\n- Give the reply in short and crisp tone, keep the reply short as a normal human\n- dont reveal that you are an ai, return a response like a human being and if something is asked out of the given information, tell that you dont know\n- If asked to make changes to the story, ask the user to ask the same to gemma as you dont hae the authority to make changes to the same\n- If the message is in some other langugae (written in english font), you should reply in the same language but the text should be strictly in english font only"
    response = model.generate_content(prompt, safety_settings=safe)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return generateErrorResponse(prompt)
    
def editStory(story: str, prompt: str):
    prompt = f"You are an AI Agent tasked with making changes to the story provided in HTML Format. Your task is to go through the HTML formatted story, understand the context and make the changes in the story according to the prompt\nStory: {story}\n\nPrompt: {prompt}\n\n\nInstructions:\n- You have to return the complete story as one response\n- You should strictly return the response in HTML format\n- Make changes in the story and give me only the story in html format\n- You should separate different paragraphs in <p></p> tags\n- you should create headings using <h1> tags and subheadings using <h2>, <h3> and all\n- Important elements like bold elements and italic elements should be wrapped with their respective <b> and <i> tags\n- If the story is empty, create the story from beginning following the above restrictions\n- If the prompt is irrelevant to the story, or is inappropriate in any kind, you should return the story unchanged back\n- the response should only contain the story response, notthing else should be added as suggestion"
    response = model.generate_content(prompt, safety_settings=safe)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        text_content = str(text_content).replace("\n","").replace("\"","'").replace("\'","'")
        return text_content
    except Exception as e:
        print(e)
        return generateErrorResponse(prompt)
    
def makeImagePrompt(story:str, chunk: str):
    prompt = f"You are an AI Agent tasked with Prompt Engineer tasks, you are provided with a chunk of story, you need to create an Image for the provided chunk, create a prompt for the required image that would best suit the case\nStory: {story}\nChunk: {chunk}\nInstructions:\n- Ig the chunk is empty, you should return a prompt for creating an image showing no chunk\n- If the chunk contains invalid data, you should return a prompt for creating image for showing that the chunk containes invalid data\n- revise the prompt to be safe for the image generator AI, the refined prompt should follow all the safety rules for AI Generation\n- the refined prompt should contain all the information that relates with the story"
    response = model.generate_content(prompt, safety_settings=safe)
    try:
        candidate = response.candidates[0]
        content = candidate.content
        text_content = content.parts[0].text
        return text_content
    except Exception as e:
        print(e)
        return generateErrorResponse(prompt)
    
import os
import httpx
from openai import AzureOpenAI
import json

# Initialize the AzureOpenAI client
client = AzureOpenAI(
    api_version="2024-02-01",
    api_key="274bfc3a00214f9eaace7f684a5b2b57",
    azure_endpoint="https://projectinnovate.openai.azure.com/"
)

def generate_image(prompt: str) -> str:
    """
    Generate an image using the DALL-E 3 model and return the image URL.

    :param prompt: Text description for generating the image.
    :return: URL of the generated image.
    """
    try:
        # Generate image with the given prompt
        result = client.images.generate(
            model="dall-e-3",  # the name of your DALL-E 3 deployment
            prompt=prompt,
            n=1
        )

        print("formed result")

        # Parse the response JSON
        json_response = json.loads(result.model_dump_json())
        
        # Get the image URL
        image_url = json_response["data"][0]["url"]
        
        return image_url

    except Exception as e:
        print(f"Error generating image: {e}")
        return None