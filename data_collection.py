import time
class Wheel:
    def __init__(self) -> None:
        self.speed = 0
        self.clockwise = True
        self.power = False
        
    def setSpeed(self, speed):
        self.setSpeed = speed
        
    def start(self):
        self.power = True

    def getStatus(self):
        return {'speed':self.speed, 'clockwise':self.clockwise, 'power':self.power}



class Steering:
    def  __init__(self) -> None:
        self.angle = 0 
    
    def setAngle(self, angle):
        self.angle = angle
    
    def getStatus(self):
        return {'angle':self.angle}


class CarDrive:
    def __init__(self) -> None:
        self.flwheel = Wheel()
        self.frwheel = Wheel()
        self.blwheel = Wheel()
        self.brwheel = Wheel()
        self.direction = Steering()
     
    def start(self):
        self.flwheel.start()
        self.frwheel.start()
        self.blwheel.start()
        self.brwheel.start()
     
    def setSpeed(self, speed):
        self.flwheel.setSpeed(speed)
        self.frwheel.setSpeed(speed)
        self.blwheel.setSpeed(speed)
        self.brwheel.setSpeed(speed)
     
    def setAngle(self, angle):
        self.direction.setAngle(angle)

    
    def getStatus(self):
        fl = self.flwheel.getStatus()
        fr = self.frwheel.getStatus()
        bl = self.blwheel.getStatus()
        br = self.brwheel.getStatus()
        d = self.direction.getStatus()
        
        return {"frontleft": fl, "frontright": fr, "backleft": bl, "backright": br, "direction": d, "timestamp": time.time()}
    
    
car = CarDrive()

print(car.getStatus())

car.start()

print(car.getStatus())


car.setSpeed(50)

print(car.getStatus())


car.setAngle(20)
 
print(car.getStatus())
