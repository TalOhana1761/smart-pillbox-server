import time
import datetime
import databaseConstructor as db
import servosControls
import audioMessagePlay
import cameraRoutine
import RPi.GPIO as gpio

# This program handles the message decodings.
# 1 - write to database --- > (type) x (day) x (hour) x (minute) x (medicines) ... returns nothing
# 2 - delete from database --- > (type) x (day) x (hour) x (minute)  ... returns nothing
# 3 - manual dispensing --- > (type) x (medicines)  ... returns motor number list
# 4 - save settings --- > (type) ! (email address) ! (speaker volume) x (camera notification time) ... returns nothing

dayDict = {"1":"sunday" , "2":"monday" , "3":"tuesday" , "4":"wednsday" , "5":"thursday" , "6":"friday" , "7":"saturday"}
medDict = {"0":"1", "1":"2", "2":"3", "3":"4"}
email = "talnew1761@gmail.com"
audioVolume = 0
cameraTime = 0

def cleanList(theList):
    return [value for value in theList if value != ""]

def messageDecoding(message):
    if len(str(message)) < 1:
        return 0
    
    if message[0] == "1":
        if message[2] != "0" and int(message[2]) <= 7:
            msgList = message[2:].split("x")
            day = int(msgList[0])
            hour = int(msgList[1])
            minute = int(msgList[2])
            med = medicineDecoding(msgList[3])
            db.write([day , hour, minute , med])
            
    if message[0] == "2":
        msgList = message[2:].split("x")
        day = msgList[0]
        hour = msgList[1]
        minute = msgList[2]
        db.delete(day,hour,minute)
        
    if message[0] == "3":
        msgList = message[2:]
        med = cleanList(medicineDecoding(msgList).split("."))
        for i in range(len(med)):
            servosControls.setMotors(int(med[i]))
            print("lol" + str(i))
        audioMessagePlay.playAudioMessage()
        savedEmail = open("emailReg.txt" , "r")
        email = savedEmail.read()
        savedEmail.close()
        print(email)
        cameraRoutine.runRoutine(email)
        
    if message[0] == "4":
        print("hahaha")
        msgList = message[2:].split("!")
        email = msgList[0]
        audioVolume = float(msgList[1]) / 10
        print(audioVolume)
        cameraTime = msgList[2]
        savedEmail = open("emailReg.txt" , "w")
        savedEmail.write(email)
        savedEmail.close()
        savedVolume = open("audioVolume.txt" , "w")
        savedVolume.write(str(audioVolume))
        savedVolume.close()
        savedCameraTime = open("cameraTime.txt" , "w")
        savedCameraTime.write(str(cameraTime))
        savedCameraTime.close()
        

def medicineDecoding(med):
    finalMed = ""
    for i in range(len(med)):
        if med[i] != '0':
            finalMed += med[i] + "."
    return finalMed[:(len(finalMed)-1)]

