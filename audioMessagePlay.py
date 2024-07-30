import RPi.GPIO as gpio
import serial
import pygame
import time

def playAudioMessage():
    savedVolume = open("audioVolume.txt" , "r")
    volume = savedVolume.read()
    savedVolume.close()
    if volume == "":
        volume = 0
    path = 'messageAudio.wav'
    pygame.mixer.init()
    print(float(volume))
    pygame.mixer.music.set_volume(float(volume))
    pygame.mixer.music.load(path)
    gpio.setmode(gpio.BOARD)
    gpio.setup(18,gpio.OUT)
    gpio.output(18,1)
    pygame.mixer.music.play()
    time.sleep(4)
    if(pygame.mixer.music.get_busy() != 1):
        gpio.output(18,0)
    

