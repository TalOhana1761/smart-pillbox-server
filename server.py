from socket import *
import RPi.GPIO as gpio
import servosControls
import cameraRoutine
import audioMessagePlay
import messageDecode
import time
import datetime
import databaseConstructor as db

# This RPi uses the ip address: 10.0.0.4 and router number 10.0.0.138
# remember to change the router number when using a different network when showing in school!!!
# motor data output pins are at pins 11 13 15 16
# speaker enable output is at pin 18

def checkDateMatch(hour, minute):
    if(datetime.datetime.now().hour == hour and datetime.datetime.now().minute == minute):
        return True
    return False

def getToday():
    if datetime.datetime.now().weekday() == 6:
        return 1
    return datetime.datetime.now().weekday() + 2

def cleanList(theList):
    return [value for value in theList if value != ""]

servosControls.setupForMotors()

savedEmail = open("emailReg.txt" , "r")
email = savedEmail.read()
savedEmail.close()
db.setup()

todaysIndexFile = open("todaysIndex.txt" , "r")
todayIndex = todaysIndexFile.read()
print(todayIndex)
if todayIndex == '':
    todayIndex = 0
todaysIndexFile.close()

cameraTime = messageDecode.cameraTime
today = ''
exceptionFlag = 0

host = ''
portNumber = 21334
bufferSize = 1024
ADDR = (host,portNumber)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(5)
serverSocket.settimeout(0.5)

while True:
    try:
        #print('Waiting for connection')
        tcpCliSock , addr = serverSocket.accept()
        print('... got a connection from: ' , addr)
        data = ''
        data = tcpCliSock.recv(portNumber).decode('UTF-8')
        print(data)
        if not data:
            break
        messageDecode.messageDecoding(data)
    except:
        exceptionFlag = 1
    
    if exceptionFlag == 1:
        if today != getToday():
            todayIndex = 0
        today = getToday()
        if db.read(getToday(),todayIndex) != 0:
            meds = db.read(getToday(),todayIndex)[0]
            hour = db.read(getToday(),todayIndex)[1]
            minutes = db.read(getToday(),todayIndex)[2]
            if checkDateMatch(hour,minutes):
                medNotClean = messageDecode.medicineDecoding(meds).split(".")
                med = cleanList(medNotClean)
                print(med)
                for i in range(len(med)):
                    print(med[i])
                    servosControls.setMotors(int(med[i]))
                audioMessagePlay.playAudioMessage()
                todayIndex = todayIndex + 1
                todaysIndexFile = open("todaysIndex.txt" , "w")
                todaysIndexFile.write(str(todayIndex))
                todaysIndexFile.close()
                exceptionFlag = 0
            
serverSocket.close()