import gevent
import pyttsx3 # pip install pyttsx3 == text data into speech
import speech_recognition as sr # pip install SpeechRecognition 
import requests
from nltk.tokenize import word_tokenize
import eel
from jproperties import Properties
import json

@eel.expose
def submitTrade(data):
    print(data)
    URL = "http://127.0.0.1:5000/bookTrade/"    
    try:
        r = requests.post(URL,json=data)        
        eel.displayResult(r.text)
        speak(r.text)
        print('SUCCESS')    
        eel.displayResult('')    
        return r.text      
    except Exception as e:
        print('FAILED')
        print(e)
        return 'FAILED'

@eel.expose
def getLiveRate(query):
    URL = "http://127.0.0.1:5000/getLiveRate/"
    try:
        r = requests.get(url = URL+query)
        eel.displayAllInRate(r.text)
        print(r.text)
        speak(r.text)  
        eel.displayAllInRate('')
        print('SUCCESS')  
        
    except Exception as e:  
        print('FAILED')      
        print(e) 
        eel.displayAllInRate('FAILED')

@eel.expose
def bookTrade():
    # api-endpoint
    configs = Properties()
    with open('tradeData.properties', 'rb') as read_prop:
        configs.load(read_prop)      
    prop_view = configs.items()
    print(type(prop_view))    
    data = {}
    for item in prop_view:
        print(item)
        data[item[0]]=item[1]
    jsonStr = json.dumps(data)
    print(jsonStr)
    eel.populateTradeDetails(jsonStr)
    speak("Based on the historical data we have populated the trade details , please check and modify if required.")    

@eel.expose
def getInfo(query):
    # api-endpoint
    URL = "http://127.0.0.1:5000/getInfo/"
    try:
        r = requests.get(url = URL+query)
        eel.displayResult(r.text)
        print(r.text)
        speak(r.text)  
        eel.displayResult('')
        print('SUCCESS')  
        
    except Exception as e:  
        print('FAILED')      
        print(e) 
        eel.displayResult('FAILED')          

@eel.expose
def processCommand(query):
    if 'populate' in query:
        return bookTrade()
    elif 'rate' in query:
        return eel.getLiveRate()
    elif 'submit' in query:
        return eel.submitTrade()
    else:
        return getInfo(query)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommandCMD():
    query = input("please tell me how can I help you\n")
    return query

@eel.expose
def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.displayMessage("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing..")
        eel.displayMessage("Recognizing..")
        query = r.recognize_google(audio, language="en-IN")
        print(query)
        eel.displayMessage(query)
    except Exception as e:
        print(e)
        speak("Say that again Please...") 
        query = "Error"       
    return query

def openUI():    
    eel.start("home.html", size =(1000,800),port=9000)    

@eel.expose
def giveCommand():
    speak("Hi How can I help you? Speak once you see the prompt")  
    return takeCommandMic().lower()  
    # return bookTrade()

# from speech_recognition import Microphone as source
engine = pyttsx3.init()

if __name__== "__main__":    
    eel.init("D:\HackathonProject\AI_Assistance\Client\www")    
    openUI()