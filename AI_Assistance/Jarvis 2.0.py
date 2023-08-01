import pyttsx3 # pip install pyttsx3 == text data into speech
import datetime
import speech_recognition as sr # pip install SpeechRecognition 
import smtplib
from secrets_1 import sendersmail,epwd, to
from email.message import EmailMessage
import pyautogui
import webbrowser as web
from time import sleep
import wikipedia
import pywhatkit
import requests
from newsapi import NewsApiClient
import clipboard
from nltk.tokenize import word_tokenize
# from speech_recognition import Microphone as source
# Open ai API key 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

engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def getVoices(voice):
    voices = engine.getProperty('voices')
    if voice == 1:
        engine.setProperty('voice', voices[0].id)
        speak("This is Saaanvi")
    else:
        engine.setProperty('voice', voices[1].id)
        speak("This is Saaanvi")
   

def time() : 
    Time = datetime.datetime.now().strftime("%I:%M:%S")# hour = I minutes = M seconds = S
    speak("Current time is")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("Current date is")
    speak(day)
    speak(month)
    speak(year)
# while True:
#     audio = int(input("For male voice press 1\nFor femail voice press 2.\n"))
#     getVoices(audio);

# time()
# date()

def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good morning sir")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon sir")
    elif hour >= 18 and hour < 24:
        speak("Good evening sir")
    else: 
        speak("Good night sir")
    
def wishme():
    speak("Welcome back Raj")
    time()
    date()
    greeting()
    speak("Saanvi at your service, please tell me how can I help you")

# wishme()

def takeCommandCMD():
    query = input("please tell me how can I help you\n")
    return query
def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language="en-IN")
        print(query)
    except Exception as e:
        print(e)
        speak("Say that again Please...")
        return "None"
    return query

def sendEmail(receiver, subject, content):
    server = smtplib.SMTP('smtp.gmail.com',587) # GMAIL
    # server = smtplib.SMTP('smtp.rediffmailpro.com',586) # REDIFFMAIL
    server.starttls()
    server.login(sendersmail, epwd)
    email = EmailMessage()
    email['From'] = sendersmail
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(content)
    server.send_message(email)
    server.close()

def sendwhatsmsg(phone_no, message):
    Message = message
    web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(25)
    pyautogui.press('enter')

def searchgoogle():
    speak('What should I search for?')S S
    search = takeCommandCMD()
    web.open('https://www.google.com/search?q='+search)

def news():
    newsapi = NewsApiClient(api_key='13d703f45d4e461caed9731ffba218e4')
    speak('What topic you need the news about?')
    topic = takeCommandMic()
    data = newsapi.get_top_headlines(q=topic,
                                     language='en',
                                     page_size=5)
    newsdata = data['articles']
    for x,y in enumerate(newsdata):
        print(f'{y["description"]}')
        speak(f'{y["description"]}')
    
    speak("thats it for now i'll update you later")

def text2speech():
    text = clipboard.paste()
    print(text)
    speak(text)


# http://api.openweathermap.org/data/2.5/weather?q={City name}&units=imperial&appid={API_KEY_HERE}
# https://api.openweathermap.org/data/2.5/weather?q=Gulbarga&appid=ba1530a786c8e4363c4aba6a85124c15
# https://api.openweathermap.org/data/2.5/weather?q=Mumbai&units=imperial&appid=ba1530a786c8e4363c4aba6a85124c15
# NEW API Key : 13d703f45d4e461caed9731ffba218e4

if __name__== "__main__":
    getVoices(2)
    # wishme()      
    while True:
        # query = takeCommandCMD().lower()
        query = takeCommandMic().lower()
        # query = word_tokenize(query)
        print( query)
        
        if 'time' in query:
            time()
        
        elif 'date' in query:
            date() 
        elif 'email' in query:
            email_list = {
                'Raj':'raj.gastgar@gmail.com'
            }
            try:
                speak("To whome you want to send the mail")
                name = takeCommandMic()
                receiver = email_list[name]
                speak("What is the suject of the mail")
                subject = takeCommandMic() 
                speak('what should i say?')
                content = takeCommandMic()
                sendEmail(receiver, subject, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("unable to send the email")
        
        elif 'message' in query:
            user_name = {
                'sister' : '+91 81979 22292',
                'wife' : '+91 95915 10123',                
            }
            try:
                name = 'None'
                while(name == 'None'):
                    speak("To whome you want to send the whatsapp message ?")
                    name = takeCommandMic()
                
                phone_no = user_name[name]
                speak("What is the message")
                message = takeCommandMic() 
                sendwhatsmsg(phone_no, message)
                speak("Message has been sent")
            except Exception as e:
                print(e)
                speak("unable to send the message")

        elif 'wikipedia' in query:
            speak("searching on wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences = 2)
            print(result)
            speak(result)

        elif 'search' in query:
            searchgoogle()
        
        elif 'youtube' in query:
            speak("What should I search for on youtube?")
            topic = takeCommandMic()
            pywhatkit.playonyt(topic)

        elif 'offline' in query:
            speak("Bye Bye, Be Happy")
            quit()
        
        elif 'weather' in query:
            speak("Which city's weather you want to know");
            city = takeCommandMic()
            url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=ba1530a786c8e4363c4aba6a85124c15'
            res = requests.get(url)
            data = res.json()
            weather = data['weather'] [0] ['main']
            temp = data['main']['temp']
            desp = data['weather'] [0]['description']
            temp = round((temp - 32) * 5/9)
            print(weather)
            print(temp)
            print(desp)      
            speak(f'weather in {city} like')
            speak('Temperature : {} degree celcius'.format(temp))
            speak('weather is : {} '.format(desp))

        elif 'news' in query:
            news()

        elif 'read' in query:
            text2speech()
        
        elif 'created' in query:
           speak("Aadayaa this software is created by your kaakaa Raajeshwaar, he created me.")

        elif 'none' in query:
            speak("Talk after Listening shown on the command prompt")
        
        else:            
            query = "about " + query
            result = wikipedia.summary(query, sentences = 2)
            print(result)
            speak(result)