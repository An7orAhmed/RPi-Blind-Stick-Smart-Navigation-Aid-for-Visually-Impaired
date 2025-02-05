import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def say(text):
    engine.say(text)
    engine.runAndWait()
    
say("My name is antor")