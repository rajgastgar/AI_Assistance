import gevent
import pyttsx3 # pip install pyttsx3 == text data into speech
import speech_recognition as sr # pip install SpeechRecognition 
import requests
from nltk.tokenize import word_tokenize
import eel
from jproperties import Properties
import json
import re

# <CUST_ID>:<B/S Indicator>:<CCY/CTR>:<Type i.e. SPOT,FWD>
# <TRADE_ID>
# cmrName=<Customer name>;ctr=<CTR> ctrAmount=<CTR amount>>

tradeBookKeywords = [];
tradeEnquiryKeywords = [];
analysisKeywords = ["analysis","data","analyse"];
tradeBookRegex = re.compile(r'\d{4}:(B|S):(\w{3}/\w{3}):(SPOT|FWD)')
tradeEnquiryRegex = re.compile(r'\b\d{7}\b')
analysisRegex = re.compile(r'(analyse) \b(ctr|ccy|cmrName|valueDate)\b')
speechMode = False


def showAnalysis(query):
    URL = "http://127.0.0.1:5000/showAnalysis/"    
    try:
        requests.get(URL+query)        
        eel.displayResult("Chart shown")        
    except Exception as e:
        print('FAILED')
        print(e)
        return 'error'

@eel.expose
def prepareAndSubmitTrade(query):
    eel.prepareTradeDataObj(re.split(':', query))(callback_prepareAndSubmitTrade)

def callback_prepareAndSubmitTrade(output):
    return output

@eel.expose
def setSpeechMode(val):
    global speechMode
    speechMode = val

@eel.expose
def submitTrade(data):
    print(data)
    URL = "http://127.0.0.1:5000/bookTrade/"    
    try:
        r = requests.post(URL,json=data)        
        eel.displayResult(r.text)
        if(speechMode):
            speak(r.text[:100])
        print('SUCCESS')    
        eel.displayResult('')    
        return r.text      
    except Exception as e:
        print('FAILED')
        print(e)
        return 'error'

@eel.expose
def getLiveRate(query):
    URL = "http://127.0.0.1:5000/getLiveRate/"
    try:
        r = requests.get(url = URL+query)
        eel.displayAllInRate(r.text)
        print(r.text)
        speak(r.text[:100])  
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
    if(speechMode):
        speak("Trade details are now populated.")    

@eel.expose
def populateCommands():
    # api-endpoint
    configs = Properties()
    with open('helpCommands.properties', 'rb') as read_prop:
        configs.load(read_prop)      
    prop_view = configs.items()
    print(type(prop_view))    
    data = {}
    tradeBookKeywords.clear
    tradeEnquiryKeywords.clear

    for item in prop_view:
        print(item)
        data[item[0]]=item[1]
        if(item[0].startswith('tradeBookingSpeech')):
            appendMoreStrings(tradeBookKeywords, item[1].data.lower())
        elif(item[0].startswith('tradeEnquirySpeech')):
            appendMoreStrings(tradeEnquiryKeywords, item[1].data.lower())          
    jsonStr = json.dumps(data)
    print(jsonStr)
    eel.populateHelpCommands(jsonStr)      

@eel.expose
def savePropertiesValues(data1):  
    data =  json.loads(data1);  
    # print("savePropertiesValues "+data)
    configs = Properties()
    configs["tradeBookingCmd"] = data['tradeBookingCmd']
    configs["tradeBookingSpeech"] = data['tradeBookingSpeech']
    configs["tradeEnquiryCmd"] = data['tradeEnquiryCmd']
    configs["tradeEnquirySpeech"] = data['tradeEnquirySpeech']  

    tradeBookKeywords.clear
    tradeEnquiryKeywords.clear

    appendMoreStrings(tradeBookKeywords, data['tradeBookingSpeech'].lower())
    appendMoreStrings(tradeEnquiryKeywords, data['tradeEnquirySpeech'].lower()) 

    print("tradeBookKeywords ",tradeBookKeywords)
    print("tradeEnquiryKeywords ",tradeEnquiryKeywords)

    with open("helpCommands.properties", "wb") as f:
        configs.store(f, encoding="utf-8")
    return "Properties saved !!"

@eel.expose
def getInfo(query):
    # api-endpoint
    URL = "http://127.0.0.1:5000/getInfo/"
    try:
        r = requests.get(url = URL+query)
        eel.displayResult(r.text)
        print(r.text)
        if(speechMode):
            speak(r.text[:100])  
        eel.displayResult('')
        print('SUCCESS')  
        return r.text
    except Exception as e:  
        print('FAILED')      
        print(e) 
        eel.displayResult('FAILED')   
        return "Error"

@eel.expose
def tradeEnquiry(query):
    print("Inside tradeEnquiry" + query)
    # api-endpoint    
    URL = "http://127.0.0.1:5000/getTradeDetails/"
    try:
        r = requests.get(url = URL+query)
        eel.displayResult(r.text)
        print(r.text)
        if(speechMode):
            speak(r.text[:100])          
        print('SUCCESS')  
        return r.text;     
    except Exception as e:  
        print('FAILED')      
        print(e) 
        eel.displayResult('FAILED')    
        return "Something went wrong"      

@eel.expose
def processCommand(query):
    queryList = word_tokenize(query)
    print(queryList)
    print("tradeBookKeywords ",tradeBookKeywords)
    print("tradeEnquiryKeywords ",tradeEnquiryKeywords)
    for q in queryList:
        if q in tradeBookKeywords:        
            return bookTrade() 
        elif q in analysisKeywords:
            return showAnalysis("ctr")
        elif q in tradeEnquiryKeywords:  
            print("Inside enquiry")
            res = ''.join(filter(lambda i: i.isdigit(), query))
            res = res.strip()
            print("query :"+res)
            if(res.isnumeric()):
                return tradeEnquiry(res)
            else:
                if(speechMode):
                    speak("Only numberic values are allowed")
                return "Only numberic values are allowed"         

    return getInfo(query)

@eel.expose
def processCmdInput(query):
    if(tradeBookRegex.match(query)):
        return prepareAndSubmitTrade(query)
    elif(tradeEnquiryRegex.match(query)):
        return tradeEnquiry(query)
    elif(analysisRegex.match(query)):
        query = query.replace("analyse","")
        query = query.strip()
        showAnalysis(query)
        return "Showing chart"
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
        eel.displayListeningIcon()
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
    speak("Hi How can I help you?")  
    return takeCommandMic().lower()  
    # return bookTrade()

def appendMoreStrings(list, strToBeAdded):
    newWords = word_tokenize(strToBeAdded)
    for nw in newWords:
        list.append(nw)

# from speech_recognition import Microphone as source
engine = pyttsx3.init()

if __name__== "__main__":    
    eel.init("D:\HackathonProject\AI_Assistance\Client\www")    
    openUI()