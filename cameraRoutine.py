import yagmail
import keyring
from picamera2 import Picamera2
import libcamera
import time

# This program takes recieves an email address, take a picture of dispensed pills and send to given Email

def runRoutine(clientEmail):
    yag = yagmail.SMTP("talsRaspberryEmail" , 'puzcjkehbqxlcokh')
    to = clientEmail
    subject = "Smart PillBox notification"
    body = [yagmail.inline("/home/tal176/python scripts/pic.jpg")]
    
    camera = Picamera2()
    #config = camera.create_preview_configuration(main={"size":(1920,1080)})
    config = camera.create_preview_configuration()
    config["transform"] = libcamera.Transform(hflip=0,vflip=0)
    camera.configure(config)
    
    if clientEmail != "":
        camera.start()
        time.sleep(1)
        camera.capture_file("pic.jpg")
        camera.close()
        yag.send(to,subject,body)

