import speech_recognition as sr
import edge_tts
import asyncio
import pygame
import tempfile
import os
import webbrowser
import datetime
import subprocess

pygame.mixer.init()


# -------------------- Text To Speech --------------------

async def speak_async(text):
    print("Assistant:", text)

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    filename = file.name
    file.close()

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-NeerjaNeural"
    )

    await communicate.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove(filename)


def speak(text):
    asyncio.run(speak_async(text))


# -------------------- Greeting --------------------

def greet():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good Morning!")

    elif hour < 17:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am your personal assistant. How can I help you?")


# -------------------- Listen --------------------

recognizer = sr.Recognizer()

recognizer.pause_threshold = 0.8
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True


def take_command():

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(source, duration=2)

        try:

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:
            return ""

    try:

        print("Recognizing...")

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("You:", command)

        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
        return ""

    except sr.RequestError:
        speak("Please check your internet connection.")
        return ""


# -------------------- Commands --------------------

def execute(command):

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif "open github" in command:
        webbrowser.open("https://github.com")
        speak("Opening GitHub")

    elif "open linkedin" in command:
        webbrowser.open("https://www.linkedin.com")
        speak("Opening LinkedIn")

    elif "open chatgpt" in command or "open chat g p t" in command:
        webbrowser.open("https://chat.openai.com")
        speak("Opening ChatGPT")

    elif "search google for" in command:

        query = command.replace(
            "search google for",
            ""
        ).strip()

        webbrowser.open(
            "https://www.google.com/search?q=" + query
        )

        speak("Searching Google for " + query)

    elif "search youtube for" in command:

        query = command.replace(
            "search youtube for",
            ""
        ).strip()

        webbrowser.open(
            "https://www.youtube.com/results?search_query=" + query
        )

        speak("Searching YouTube for " + query)

    elif "time" in command:

        current = datetime.datetime.now().strftime("%I:%M %p")

        speak("The time is " + current)

    elif "date" in command:

        today = datetime.datetime.now().strftime("%d %B %Y")

        speak("Today's date is " + today)

    elif "open calculator" in command:

        subprocess.run(["open", "-a", "Calculator"])

    elif "open terminal" in command:

        subprocess.run(["open", "-a", "Terminal"])

    elif "open visual studio code" in command or "open vs code" in command:

        subprocess.run(["open", "-a", "Visual Studio Code"])

    elif (
        "exit" in command
        or "quit" in command
        or "bye" in command
        or "goodbye" in command
        or "stop" in command
    ):

        speak("Goodbye. Have a nice day.")

        return False

    else:

        speak("Sorry, I don't know how to do that.")

    return True


# -------------------- Main --------------------

def main():

    greet()

    while True:

        command = take_command()

        if command == "":
            continue

        if not execute(command):
            break


if __name__ == "__main__":
    main()
   
  
