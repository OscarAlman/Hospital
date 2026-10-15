class Hospital:
    def __init__(self,name,employees=[]):
        self.name=name
        self.employees=employees
    
    def add_employee(self,employee):
        self.employees.append(employee)

class Employee:
    def __init__(self,parameterName):
        self.name=parameterName
    
    
class Doctor(Employee):
    def __init__(self,parameterName,parameterSpecialty):
        super().__init__(parameterName)
        self.specialty=parameterSpecialty    


drSmith= Doctor(parameterName="Dr Smith",parameterSpecialty="Neuro")
drJones= Doctor(parameterName="Mr Jones",parameterSpecialty="HeartSurgeon")
                
george=Hospital("St Georges Hospital", [drSmith, drJones])

drDave = Doctor(parameterName="Mr Dave",parameterSpecialty="TraumaSurgeon")
print(george.name) 
george.add_employee(drDave)
print(george.employees) 