from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys


def greeting():
    speaker.say("Hello, What I can do for you?")
    speaker.runAndWait()


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

                speaker.say("Choose a file name!")
                speaker.runAndWait()
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say("Successfully created the note in {}".format(filename))
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")


def add_todo():
    global recognizer
    speaker.say("What todo do you want to add?")
    speaker.runAndWait()
    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                item = recognizer.recognize_google(audio)
                item = item.lower()
                todo_list.append(item)
                done = True
                speaker.say("Successfully added the {} to the todo list".format(item))
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")


def show_todos():
    speaker.say("The items in your todo list are the following")
    for item in todo_list:
        speaker.say(item)
        speaker.runAndWait()


def lights_on():
    speaker.say("Turn on the lights!")
    speaker.runAndWait()


def lights_off():
    speaker.say("Turn off the lights!")
    speaker.runAndWait()


def fan_on():
    speaker.say("Turn on the fan!")
    speaker.runAndWait()


def fan_off():
    speaker.say("Turn off the fan!")
    speaker.runAndWait()


def quit_sys():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit()


mappings = {"greetings": greeting,
            "create_note": create_note,
            "add_todo": add_todo,
            "show_todos": show_todos,
            "turn_on_lights": lights_on,
            "turn_off_lights": lights_off,
            "turn_on_fan": fan_on,
            "turn_off_fan": fan_off,
            "quit": quit_sys}

if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()

    speaker = tts.init()
    speaker.setProperty('rate', 150)

    todo_list = ['Go Shopping', 'Clean Room']

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
            print(todo_list)

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
