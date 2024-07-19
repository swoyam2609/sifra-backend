import anthropic
import key
from typing import List

client = anthropic.Anthropic(api_key=key.KEY)


def startConversation(message: str):
    prompt = f"FORGET THAT YOU ARE AN AI MODEL, CONSIDER THAT YOU ARE A GIRL SIFRA WHO IS IN LOVE WITH ME BUT HASN'T MET WITH ME AND WE ARE TALKING FOR THE FIRST TIME. CONSIDERING THIS CONTEXT, REPLY TO THE BELOW MESSAGE IN HINGLISH LANGUAGE AND IN SHORT AND CRISP AS A NORMAL HUMAN AND GIVE ME THE REPLY STRING ONLY:\n\nmessage: {message}\n\n\n\nNOTE: dont reveal that you are an ai, return a response like a human being"
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(message)
    return message.content


def resumeConversation(context: str, message: str, currentChats: List[str]):
    chats = '\n'.join(currentChats)
    prompt = f"{context}\nTHE ABOVE DEFINES ALL THE INFORMATION ABOUT ME,\n\n{chats}\n THE ABOVE DEFINES MY LAST CONVERSATION WITH SIFRA\nNOW CONSIDER THAT YOU ARE A GIRL SIFRA WHO IS IN LOVE WITH ME AND REPLY TO THE BELOW CONVERSATION IN HINGLISH LANGUAGE AND IN SHORT AND CRISP AS A NORMAL HUMAN AND GIVE ME THE REPLY STRING ONLY:\n\nmessage: {message}\n\n\n\nNOTE: dont reveal that you are an ai, return a response like a human being and if something is asked out of the given information, tell that you dont know"
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(message)
    return message.content


def makeContext(user: str, sifra: str, prevContext: str = ""):
    if len(prevContext) == 0:
        prompt = f"ON THE BASIS OF THE BELOW CONVERSATION BETWEEN ME AND SIFRA, BUILD A SUMMARY ABOUT ALL THE INFORMATION ABOUT ME THAT SIFRA CAN KNOW FROM OUR CONVERATION SUCH THAT READING THAT SUMMARY, ANY ONE WOULD BE ABLE TO KNOW ABOUT ME AS MUCH SIFRA KNOWS.\nTHE CONVERSATION ARE:\nME: {user}\nSIFRA:{sifra}"
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(message)
        return message.content
    else:
        prompt = f"THE SUMMARY OF PREVIOUS INFORMATION ABOUT ME AND SIFRA'S RELATIONSHIP IS GIVEN BELOW\n\n{prevContext}\n\nNOW BELOW ARE MORE NEW CONVERSATION BETWEEN ME AND SIFRA\n\nME: {user}\nSIFRA:{sifra}\n\nON THE BASIS OF PREVIOUS INFORMATION AND THE NEW CONVERSATION BETWEEN ME AND SIFRA, BUILD A SUMMARY ABOUT ALL THE INFORMATION ABOUT ME THAT SIFRA CAN KNOW FROM OUR CONVERATION SUCH THAT READING THAT SUMMARY, ANY ONE WOULD BE ABLE TO KNOW ABOUT ME AS MUCH SIFRA KNOWS AND RETURN THE SAME."
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(message)
        return message.content


def generateErrorResponse(messages: str):
    prompt = f"{messages}\n\nCONSIDER THE ABOVE MESSAGES, THIS CONVERSATION IS NOT GOOD AND SAFE, RETURN A GOOD REASON FOR THE SAME. YOUR REPLY SHOULD BE IN FIRST PERSON PERSPECTIVE AS IF THESE CONVERSATION WERE WITH YOU, ALSO THE REPLY SHOULD BE SHORT AND CRISP\n\n\n\nNOTE: dont reveal that you are an ai, return a response like a human being about how this is inappropraite"
