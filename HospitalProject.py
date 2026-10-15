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


#TODO Create another subclass for Nurse
#TOTO add age to the base class , as both burses and Drs have age
#TODO Add a function at the hostpital class, to return the count of employees
#TODO Add a function at the hostpital class, to return the count of Drs
#TODO Add a function at the hostpital class, to return the count of Nurses
#TODO Add a function at the hostpital class, to print Drs only
#TODO Add a function at the hostpital class, to print Nurses only
#TODO search for a doctor by name. The search should ignore capitals (“smith” matches “Smith”), only match doctors, and give back the doctor if found or None if not.
#TODO Every method needs a docstring explaining what it does.
#TODO use __str__ so when you do print(drDave) it prints something human readable
#TODO .... for extra points use  __repr__   so when you print(employees)  it prints somethings useful





drSmith= Doctor(parameterName="Dr Smith",parameterSpecialty="Neuro")
drJones= Doctor(parameterName="Mr Jones",parameterSpecialty="HeartSurgeon")
                
george=Hospital("St Georges Hospital", [drSmith, drJones])

drDave = Doctor(parameterName="Mr Dave",parameterSpecialty="TraumaSurgeon")
print(george.name) 
george.add_employee(drDave)
print(george.employees) 