from chatterbot import ChatBot  # import the chatbot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from autocorrect import spell
import string
from chatterbot.conversation import Statement
import speech_recognition as sr
import pyttsx3
import datetime
import time
from selenium import webdriver # to control browser operations
import winsound
from chatterbot import comparisons, response_selection

"""import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)"""

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)

#bot = ChatBot("Bot")
bot = ChatBot(
    "ChatBot",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": comparisons.levenshtein_distance,
            "response_selection_method": response_selection.get_most_frequent_response
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'maximum_similarity_threshold': 0.99,
            'threshold': 0.65,
            'default_response': 'default_value'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Quiero reservar un crucero',
            'output_text': 'Puedes reservarlo ahora en: https://www.logitravel.com/cruceros/'
        },
    ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="db.sqlite3"
)
trainer = ChatterBotCorpusTrainer(bot)

corpus_path = 'F:/BackUpMyData/MySVNRepo/MyData/Tech_TargetLearns/Machine_Learning/Workspaces/MyBot/data/english/'

for file in os.listdir(corpus_path):
	trainer.train(corpus_path + file)

def speak(audio):
    print('ChatBot: ' + audio)
    engine.say(audio)
    engine.runAndWait()

def verifyHuman():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # winsound.Beep(500, 750)
        # r.pause_threshold=1
        # r.adjust_for_ambient_noise(source, duration=1)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You:" + text.strip().lower());
        return text.strip().lower()
    except sr.UnknownValueError:
        print("I'm not alive, wake me up by calling 'Alpha' ")


def getAudioMessage():
    while (True):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            flag = False
        try:
            message = r.recognize_google(audio, language='en-US').strip()
            if message:
                winsound.Beep(500, 750)  # 1000,500
                speak('Processing your input...Please wait...')
                print("You:" + message)
                if "exit" in str(message) or "bye" in str(message) or "sleep" in str(message) or "quit" in str(message):  #message.strip()
                    speak('I am signing off ! Bye, have a good day. You can wake me up any time')
                    break
                elif 'shutdown' in message:
                    speak('Good Bye !! I am no more Alive !')
                    exit()
                elif 'open' in message or 'search' in message:
                    process_text(message)
                else:
                    #reply = str(bot.get_response(message))  # if keyWord.lower() in text.lower():
                    #speak(reply)
                    reply = str(bot.get_response(message))
                    if reply is "default_value":
                        reply = str(bot.get_response('default_response'))
                    speak(reply)

        except sr.UnknownValueError:
            print("Sorry!! Say Something :(")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))


def greetMe(name):
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!' + name)

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!' + name)

    if currentH >= 18 and currentH != 0:
        speak('Good Evening!' + name)


def process_text(input):
    try:
        if "search" in input or "play" in input:
            # a basic web crawler using selenium
            search_web(input.lower())
            return

        elif "open" in input:
            # another function to open
            # different application availaible
            open_application(input.lower())
            return
        else:
            speak("I can search the web for you, Do you want to continue?")
            ans = verifyHuman()
            if "yes" in str(ans) or "yeah" in str(ans):
                search_web(input.lower())
            else:
                return
    except:
        speak("I don't understand, I can search the web for you, Do you want to continue?")
        ans = verifyHuman()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input.lower())


def search_web(input):
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()
    if 'youtube' in input:
        speak("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx + 1:]
        driver.get("http://www.youtube.com/results?search_query =" + '+'.join(query))
        return

    elif 'wikipedia' in input:
        speak("Opening Wikipedia")
        indx = input.lower().split().index('wikipedia')
        query = input.split()[indx + 1:]
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
        return

    else:
        if 'google' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q =" + '+'.join(query))

        elif 'search' in input or 'play' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q =" + '+'.join(query))
        else:
            driver.get("https://www.google.com/search?q =" + '+'.join(input.split()))
        return


# function used to open application
# present inside the system. 
def open_application(input):
    if "chrome" in input:
        speak("Google Chrome")
        os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        return

    elif "firefox" in input or "mozilla" in input:
        speak("Opening Mozilla Firefox")
        os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe')
        return

    elif "word" in input:
        speak("Opening Microsoft Word")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\\Microsoft Office Word 2007.lnk')
        return

    elif "excel" in input:
        speak("Opening Microsoft Excel")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\\Microsoft Office Excel 2007.lnk')
        return

    else:
        speak("Application not available")
        return


# Main Code
if __name__ == "__main__":
    winsound.Beep(500, 750)
    while (True):
        message = verifyHuman()
        if "none" not in str(message).lower():
            winsound.Beep(500, 750)
            if "alpha" in message or "oscar" in message:
                greetMe("")
                speak('I am your Personal Assitant Alpha Voice Bot')
                speak('Tell me, What can i do for you?')
                getAudioMessage()
            if "shutdown" in message:
                speak('Good Bye !! I am no more Alive !')
                break

    """speak("What's your name, Human?")
    while (True):
        message = verifyHuman()
        if "none" not in str(message).lower():
            speak('OK Thanks for your input, Please hold on, Verifying the identification')
            if "raja" in str(message):
                speak('Cool! Identification matches with my Neural Schema')
                speak('Thanks for your time')
                # greetMe(message)
                speak('I am your Personal Assitant - JAB')
                speak('What can i do for you?')
                getAudioMessage()
            else:
                speak('Ohhh No!, You are not authorized to use me, Sorry')
                speak('Bye, have a good day.')
            break
        else:
            speak('No User input given to me ! Try again !')
    """
