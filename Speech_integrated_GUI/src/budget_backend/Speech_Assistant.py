#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
from gtts import gTTS
from time import ctime
import pyglet
import excel_budget.budgetsheet as bs
import time
import os
from datetime import datetime, timedelta

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    filename = "/python27/audio.mp3"
    tts.save(filename)

    music = pyglet.media.load(filename, streaming = False)
    music.play()
    time.sleep(music.duration)
    os.remove(filename)

# Record Audio
def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=5)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data

# Create Global List of Categories
def createCats():
    flag = -1
    isNo = "yes"
    isYes = "no"
    global catGList
    
    while(isNo != "no" and isYes != "yes"):
        isYes = ""
        isNo = ""
        tmpData = ""

        # Bot receives the categories from user
        speak("alright, what categories would you like to add?")
        tmpData = recordAudio()
        tmpData = tmpData.split(" ")

        # Adds all new categories and handles duplicates with ignorance of "and"
        for val in tmpData:
            if ((val != "and") and (val not in catGList)):
                catGList.append(val)

        # If/Else statement for varying responses from bot       
        if (flag != 0):
            speak("do you want to add more categories?")
            isNo = recordAudio()
            flag = 0
        elif (flag != 1):
            speak("will that be all?")
            isYes = recordAudio()
            flag = -1
    
# Records the daily expenses for all categories 
def dailyRecorder():

    list = ["How much did you spend for {} today?",
            "How about {}",
            "What should I add for {}",
            "What about {}",
            "Next is {}"]
    i =0
    expTmpList = []
    # Receive the value for each category from user
    # and export to excel
    while(i < len(catGList)):
        statement = list[(len(list)%(i+1))].format(catGList[i])
        speak(statement)
        tmpData = recordAudio()
        print tmpData

        if (tmpData != ""):
            replacements = ('$', "bucks", "dollars")
            for r in replacements:
                tmpData = tmpData.replace(r, " ")
            tmpData = tmpData.split(" ")

            for val in tmpData:
                if ((val.isnumeric() and val > 0) or (val == ("zero" or "nothing"))):
                    expTmpList.append(val)
                    i+=1

    storeXL(catGList, expTmpList)

def nextDate(lastDate):
    lastDate = lastDate.split('-')
    date = datetime(int(lastDate[0]), int(lastDate[1]), int(lastDate[2]))
    newDate = date + timedelta(days=1)
    return newDate.strftime('%Y-%m-%d')

# StoreXL calls functions from budgetsheet.py to make realtime modifications to spreadsheet
def storeXL(catList, valList):
    print catList
    print valList
    lastDate = obj.get_last_row_title()
    date = nextDate(lastDate)
    if (len(valList) == len(catList)):
        for i in range(len(valList)):
            obj.write_budget_cell(date, catList[i], valList[i])        

# Stella manages all user commands for recording data
def corona(lData):
    global catGVlist

    if "create expense" in lData:
        createCats()
        print catGList
    
    elif "update my daily" in lData:
            dailyRecorder()

    else:
        catTmpList = []
        expTmpList = []
        replacements = ('$', "bucks", "dollars")
        for r in replacements:
            lData = lData.replace(r, " ")
        lData = lData.split(" ")

        for val in lData:
            if val in catGVList:
                catTmpList.append(val)
            if (val.isnumeric()):
                expTmpList.append(val)

        storeXL(catTmpList, expTmpList)      

    ##    if "how are you" in data:
    ##        speak("I am fine")
    ## 
    ##    if "what time is it" in data:
    ##        speak(ctime())
    ## 
    ##    if "where is" in data:
    ##        data = data.split(" ")
    ##        location = data[2]
    ##        speak("Hold on Ajinkya, I will show you where " + location + " is.")
    ##        os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")

# Login an existing user or a new one or skip it entirely
def login():
    #speak("Hey there! Do you want to see my creators' login feature demo or no?")
    speak("Hey there! yes or no?")
    tmpData = recordAudio()

    # If the user hasn't answered yet
    if (tmpData == ""):
        return False, ""

    # Start the login process
    elif (tmpData != "no"):
        speak("Alright! Have I seen you before or are you a new user?")
        tmpData = recordAudio()
        # existing user?
        if ("before" in tmpData.split(" ")):
            flagUser = 0

            # Definite chances of identifying your account
            while(flagUser <= 2):
                speak("What's your name?")
                tmpDataUser = recordAudio()
                if tmpDataUser in userList:
                    speak("and your pass key please?")
                    tmpDataPass = recordAudio()
                    flagPass=0

                    # Definite chances of trying your password
                    while(flagPass <= 2):
                        if (userList[tmpDataUser] == tmpDataPass):
                            speak("Alright you're in!")
                            return True, tmpDataUser
                        else:
                            if (flagPass == 0):
                                speak("oops! try again!")
                            elif flagPass == 1:
                                speak("Still not correct! last chance")    
                            tmpDataPass = recordAudio()
                            flagPass+=1
                    speak("Sorry! you've exceeded attempts, restart the program!")
                    return True, ""
                # Try agains for user name
                else:
                    speak("Did you say " + tmpDataUser + "?")
                    if (tmpData != "no"):
                       speak("Alright! Let me check that again!")
                       
                    else:
                        speak("Sorry! I didn't get your name. Let's try again!")
                    flagUser+=1

            # Ask user to sign up first
            speak("Hey I can't find you in my database. Sign up first please.")
            return True, ""
    # Do not start the login process             
    elif (tmpData == "no"):
        return True, ""

# initialization
def main():
    flag = False
    name = "User"
    time.sleep(1)
    
    while(not flag):
        flag, name = login()
    
    print(" \n")
    speak("Hi " + name + ", what can I do for you?")
    while (1):
        data = recordAudio()
        rData = data.split(" ")
        if rData[0] == "Corona":
            corona(data)
        

userList = {"Ron" : "123", "Sam":"124", "Meena":"125", "Alec":"126"}      
catGList = []
#catGList = ["groceries", "gas", "restaurants", "snacks", "shopping"]
catGVList = ["groceries", "gas", "restaurants", "snacks", "shopping", "electric", "internet", "water"]
obj = bs.BudgetSheet(os.path.join(os.getcwd(), 'data', 'test.xlsx'))
main()
