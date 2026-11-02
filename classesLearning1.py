class Transport:
    def __init__(self,name):
        self.name=name

    def go(self, weeMessage):
        print(f"we go {weeMessage}")
        
class Plane(Transport):
    def __init__(self,airline,name):
        self.airline=airline
        super().__init__(name)
        
    def __str__(self):
        return f'plane brand is {self.name} the airline is {self.airline}'
    
    
class Car(Transport):
    def __init__(self,brand,engineType,NumberOfWheels,FourWheelDrive,name):
        self.brand=brand
        self.engine=engineType
        self.NumberOfWheels=NumberOfWheels
        self.FourWheelDrive=FourWheelDrive
        super().__init__(name)
        
    def __str__(self):
        return f'the cars brand is {self.brand} the engine type is {self.engine} \n the number of wheels is {self.NumberOfWheels} \n and it is {self.FourWheelDrive}'
    
boeing=Plane('british airways','boeing')


t=Transport("this")
t.go()

boeing.go("sdfsdf")

ford=Car('ford','in line 4','4 wheels','2 wheel front wheel drive','Ford')
ford.go("ggg")

print(Ford)
