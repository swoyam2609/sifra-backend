import sounddevice as sd
import soundfile as sf
from gtts import gTTS
import os
from pathlib import Path


# Function to convert a given string into speech and save it into an audio file
def convertToSpeech(input_text: str):

    # Setting up the output path
    output_dir = Path.cwd() / "files"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "output.wav" 

    # Converting the given input string into an audio file
    try:
        speech = gTTS(text=input_text, lang="en", slow=False)
        speech.save(str(output_path)) 
        return str(output_path)
    
    # Except block to catch out any kind of error if any
    except Exception as e:
        print(f"Error occurred: {e}")
        return None




# Function to play an audio file stored at a given path
def play_audio(file_path, speed_factor):

    # Trying to read the file and play the saved audio
    try:
        data, fs = sf.read(file_path)
        new_fs = int(fs * speed_factor)
        sd.play(data, new_fs)
        sd.wait() 

    # Except block to catch out any kind of error if any
    except Exception as e:
        print(f"Error playing sound: {e}")



# Function to speak out a given text and display the same on the screen
def speak(text: str, speed_factor=1.33):

    # Conveting the text into an audio file and returning the path where it is saved
    path = convertToSpeech(text)

    # If path containes a valid path name
    if path:

        # Play the audio saved in the path
        play_audio(path, speed_factor=speed_factor)
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"🤖: {text}\n")
            except Exception as e:
                print(f"Error removing file: {e}")
        else:
            print("The file does not exist")

    # Except block to catch out any kind of error if any    
    else:
        print("Failed to convert text to speech")



# Function to print a given text with the prefix stating that this was an input command
def printUser(text: str):
    print(f"\n👨‍💻: {text}\n")