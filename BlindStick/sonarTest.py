import time
from gpiozero import LED, Button, DistanceSensor

bDist, fDist, lDist, rDist = 0, 0, 0, 0

def hardware():
    global bDist, fDist, lDist, rDist
    
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
        time.sleep(1)

        print("B:{}, F:{}, L:{}, R:{}".format(bDist, fDist, lDist, rDist))
        print("Butt:{}, LDR:{}".format(water.is_pressed, ldr.is_pressed))

        if bDist < 10 or fDist < 10 or lDist < 10 or rDist < 10:
            motor.on()
            buzzer.on()
        else:
            motor.off()
            buzzer.off()
            
if __name__ == "__main__":
    hardware()