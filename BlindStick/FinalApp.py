import os
import cv2
import FaceDetect
import gps
import time
from datetime import datetime
from threading import Thread
from gpiozero import LED, Button, DistanceSensor
import Adafruit_CharLCD as LCD
import pyttsx3
import requests

link = "http://esinebd.com/projects/rpiBlindStick/update_machine.php"

engine = pyttsx3.init()
engine.setProperty('rate', 100)

lcd = LCD.Adafruit_CharLCD(2, 3, 4, 17, 27, 22, 16, 2, 10)
    
bDist, fDist, lDist, rDist = 0, 0, 0, 0
blockHardware = 0

def hardware():
    global bDist, fDist, lDist, rDist, blockHardware
    out = False
    prevTime = 0
    
    buzzer = LED(18)
    motor = LED(8)
    water = Button(7)
    ldr = Button(1)

    left = DistanceSensor(echo=12, trigger=16, max_distance=0.99)
    time.sleep(0.5)
    right = DistanceSensor(echo=20, trigger=21, max_distance=0.99)
    time.sleep(0.5)
    bottom = DistanceSensor(echo=26, trigger=19, max_distance=0.99)
    time.sleep(0.5)
    front = DistanceSensor(echo=13, trigger=6, max_distance=0.99)
    time.sleep(0.5)
    
    while True:
        bDist = int(bottom.distance * 100)
        fDist = int(front.distance * 100)
        lDist = int(left.distance * 100)
        rDist = int(right.distance * 100)
        time.sleep(0.2)
        
        if blockHardware == 0:
            lcd.set_cursor(0, 0)
            lcd.message("D:{}, {}, {}, {}   ".format(bDist, fDist, lDist, rDist))
            lcd.set_cursor(0, 1)
            lcd.message("L:{},{}  ".format(gps.lati, gps.longi))
              
            if time.time() - prevTime >= 60:
                lcd.clear()
                print("Updating loc..")
                lcd.message("UPDATING WEB...")
                param = {"lati": gps.lati, "longi": gps.longi}
                requests.get(link, params=param)
                if ldr.is_pressed:
                    engine.say("night time")
                    engine.runAndWait()
                else:
                    engine.say("day time")
                    engine.runAndWait()
                lcd.clear()
                prevTime = time.time()
            
            if out == False:
                if water.is_pressed:
                    out = True
                    buzzer.on()
                    lcd.clear()
                    lcd.message("WATER DETECTED!")
                    engine.say("water detected")
                    engine.runAndWait()
                    buzzer.off()
                    lcd.clear()
                elif bDist < 30:
                    out = True
                    engine.say("object detected in down at " + str(bDist) + " centimeter")
                    engine.runAndWait()
                elif fDist > 30 and fDist < 50:
                    out = True
                    engine.say("object detected in front at " + str(fDist) + " centimeter")
                    engine.runAndWait()
                elif lDist < 30:
                    out = True
                    engine.say("object detected in left at " + str(lDist) + " centimeter")
                    engine.runAndWait()
                elif rDist < 30:
                    out = True
                    engine.say("object detected in right at " + str(rDist) + " centimeter")
                    engine.runAndWait()
            else:
                if bDist > 30 or fDist > 30 or lDist > 30 or rDist > 30:
                    out = False
                if water.is_pressed == False:
                    out = False
                
            if bDist < 10 or fDist < 10 or lDist < 10 or rDist < 10:
                motor.on()
                buzzer.on()
            else:
                motor.off()
                buzzer.off()
 
def main():
    global fDist, blockHardware
    FaceDetect.importFaces()
    lastDetect = ""
    
    task1 = Thread(target=gps.update)
    task1.start()
    task2 = Thread(target=hardware)
    task2.start()
    
    camera = cv2.VideoCapture(0)
    camera.set(3, 320) # width
    camera.set(4, 240) # height

    while True:
        ret, frame = camera.read()
        if ret == False: continue

        if fDist <= 30:
            print("Face Detecting...")
            blockHardware = 1
            lcd.clear()
            lcd.message("FACE DETECTING..")
            
            frame, name = FaceDetect.scan(frame)   
            print("Detected: ", name)
            lcd.set_cursor(0, 1)
            lcd.message(name)
            engine.say("face detected of " + name)
            engine.runAndWait()  
            lcd.clear()
            blockHardware = 0

        cv2.imshow('webcam LIVE', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
        
    # ------------------------
    camera.release()
    cv2.destroyAllWindows()
            
if __name__ == "__main__":
    main()