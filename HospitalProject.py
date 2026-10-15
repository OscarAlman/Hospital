class Hospital:
    def __init__(self,name,employees=[]):
        self.name=name
        self.employees=employees
    
    def add_employee(self,employee):
        self.employees.append(employee)

class Employees:
    def __init__(self,parameterName):
        self.name=parameterName
    
    
class Doctors(Employees):
    def __init__(self,parameterName,parameterSpecialty):
        super().__init__(parameterName)
        self.specialty=parameterSpecialty    

george=Hospital("George", ["Dr. Smith", "Nurse Joy", "Dr. Adams"])
        
print(george.name) 
george.add_employee("Dr. Brown")
print(george.employees) 