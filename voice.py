import openai
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
# Set your OpenAI API key
openai.api_key = "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"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said: ", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def generate_response(prompt):
    if prompt.lower() == "open google":
        webbrowser.open("https://www.google.com/")
        return "Opening Google in the default web browser"
    elif prompt.lower() == "close google":
        os.system("taskkill /f /im chrome.exe /t")
        return "Closing Google in the default web browser"
    else:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text


def is_wake_word(text):
    wake_word = "robo"

    return text.lower().startswith(wake_word)
    

while True:
    # Wait for the wake word...
    question = recognize_speech()
    if question and is_wake_word(question):
        speak("How can I help you?")
        print("Wakeword detected ")
        break

while True:
    # Wait for the question...
    question = recognize_speech()
    if question:
        if "exit" in question:
            speak("Goodbye!")
            print("Goodbye!")
            break
        response = generate_response(question)
        print("robo says:", response)
        speak(response)
