import RPi.GPIO as GPIO
import sys
import time
import numpy as np
from asciimatics.screen import ManagedScreen, Screen
from asciimatics.scene import Scene
from asciimatics.renderers import FigletText
from asciimatics.effects import  Stars
from collections import deque
from asciimatics.effects import Print, Mirage, Cycle, Wipe
from random import randint
### GPIO ###
# Set pin layout mode to board
GPIO.setmode(GPIO.BOARD)

#Global Variables
secToMin = 1/60 
RPMIndex = 0
RPM = list()
timeArr = list()
tavg = list()
counter = 0
read = 0

# Sensor Channels
sw = 38
clk = 40

# SET GPIO pin 40 to encoder A input
# SET GPIO pin 38 to switch signal
GPIO.setup(sw, GPIO.IN)
GPIO.setup(clk, GPIO.IN)

GPIO.add_event_detect(sw, GPIO.RISING)
GPIO.add_event_detect(clk, GPIO.RISING)
lastclk = GPIO.input(clk)
lastSEPress = time.time()

#initiate stars backgroun
#with ManagedScreen as screen:
def printStart(screen):
    effects = [
        Mirage(screen, FigletText("ARE YOU READY", font = 'big'), int(screen.height/5),Screen.COLOUR_YELLOW, start_frame = 10, stop_frame = 70),
        Mirage(screen, FigletText("TO CHURN?", font = 'big'), int(screen.height/2), Screen.COLOUR_YELLOW, start_frame = 10, stop_frame = 70),
        Wipe(screen, start_frame = 60),
        Stars(screen,(screen.width + screen.height))
    ]
    screen.play([Scene(effects, 150)], repeat = False)

Screen.wrapper(printStart)

def buttonPress (screen):
    effects = [
        Cycle(screen, FigletText("Button Pressed", font = 'big'), screen.height/5),
        Stars(screen, (screen.width + screen.height))
    ]
    screen.play([Scene(effects, 500)])

while(True):       
    #If the button is pressed
    #If 50 ms have passed since the last LOW, the button has been pressed again
    #If sw pin is enabled, uncomment this code
    #if GPIO.event_detected(sw):
       # if(time.time() - lastSEPress > .005):               
           # print('Button Pressed!')
           # counter = 0
        #lastSEPress = time.time()
    #If the encoder shaft is rotated
    #Added debouncer - so as not to read multiple of the same reading
    if (GPIO.event_detected(clk)):
        currentclk = GPIO.input(clk)
        timeclk = time.time()
        if(currentclk != lastclk and currentclk== 1):
            counter+=1
             #print("Counter: " + str(counter))
            timeArr.append(timeclk)
            if(counter % 20 == 0):
                for t in range(len(timeArr)-1):
                    tavg.append(timeArr[t+1]-timeArr[t])
                delT = np.mean(tavg) #in seconds
                read =(1/(delT * secToMin))
                RPM.append(read)
                print('RPM: ' + str(read))
                tavg.clear()
        lastclk = currentclk 
    time.sleep(0.001)


