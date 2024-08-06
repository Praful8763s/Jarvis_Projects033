import speech_recognition as sr
import webbrowser
import pyttsx3
import ZMusicLibrary  # Ensure this module is correctly set up with your music library
import requests
from openai import OpenAI
import os

# Initialize speech recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Define the API key for NewsAPI
newsapi_key = "<Your Key Here>"

def speak(text):
    """Use pyttsx3 to convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    """Process the command using OpenAI's GPT-3.5-turbo model"""
    client = OpenAI(api_key="<Your Key Here>")
    completion = client.Completion.create(
        model="gpt-3.5-turbo",
        prompt=f"You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please.\nUser: {command}\nJarvis:",
        max_tokens=50
    )
    return completion.choices[0].text.strip()

def processCommand(c):
    """Process the given command and execute the corresponding action"""
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open twitter" in c.lower():
        webbrowser.open("https://twitter.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open snapchat" in c.lower():
        webbrowser.open("https://snapchat.com")
    elif "open email" in c.lower():
        webbrowser.open("https://mail.google.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = ZMusicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in the library")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi_key}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Limiting to top 5 news headlines
                speak(article['title'])
        else:
            speak("Failed to fetch news")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for 'Jarvis'...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
                word = recognizer.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Jarvis Active, listening for command...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")
