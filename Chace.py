from neuralintents import GenericAssistant 
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ('I have a class', 'go have some fun', 'My exam starts soon', 'make a video')


def create_note():
    global recognizer 

    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()

    done = False 

    while not done:
         try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True 
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()
  
         except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("I did not understand you! Please Try again!")
                speaker.runAndWait()


def add_todo():

    global recognizer

    speaker.say("What todo would you want to add?")
    speaker.runAndWait()
    
    done = False 

    while not done:

        try:

            with speech_recognition.Recognize() as mic:
                
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"I added {item} to the to do list!")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("I did not understand you! Please Try again!")
                speaker.runAndWait()


def show_todo():
    
    speaker.say("The items on your to do list are the following.")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("Hello, what can i do for you today?")
    speaker.runAndWait()


def quit():
    speaker.say("Goodbye!")
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello, 
    "add_todo": add_todo,
    "create_note": create_note,
    "show_todos": show_todo,
    "exit": quit
    }

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:

    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()