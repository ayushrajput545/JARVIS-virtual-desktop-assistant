import speech_recognition as sr
import webbrowser  # inbuilt in Python
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
newsapi = os.getenv("newsapi")



# Initialize Text-to-Speech
engine = pyttsx3.init()

 
def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client= OpenAI(
    api_key= api_key
     )

    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        store=True,
        messages=[
            {"role":"system", "content":"You are virtual assistant named jarvis skilled in general tasks like alexa and google cloud"},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content


def processCommand(command):
    """Process the user's spoken command."""
    command = command.lower()  # Ensure case-insensitivity
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")
    elif "open github" in command:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
    elif "open youtube" in command:
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    
    elif command.startswith("play"):
        song= " ".join(command.split(" ")[1:])  # Extract song name
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song} in your music library.")

    elif "news" in command:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                for article in articles:
                    speak(article['title'])
            else:
                speak("No news articles found.")
        else:
            speak("Failed to fetch news. Please try again later.")
       
    
    else:
        #Let open Ai handle the request
        try:
            output = aiProcess(command)
            speak(output)
        except Exception as e:
          speak("I didn't understand that command.")


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    recognizer = sr.Recognizer()  # Create recognizer object once

    while True:
        try:
            # Listen for wake word "Jarvis"
            with sr.Microphone() as source:
                print("Listening for the wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            # Recognize speech
            word = recognizer.recognize_google(audio)
            print(f"You said: {word}")

            # Check for wake word
            if word.lower() == "jarvis":
                speak("Yes, how can I help you?")
                
                # Listen for command
                with sr.Microphone() as source:
                    print("Listening for your command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

                # Recognize and process command
                command = recognizer.recognize_google(audio)
                print(f"Command received: {command}")
                processCommand(command)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
