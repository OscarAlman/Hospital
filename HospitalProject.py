class Hospital:
    def __init__(self,name,employees=[]):
        self.name=name
        self.employees=employees
    
    def add_employee(self,employee):
        self.employees.append(employee)

george=Hospital("George", ["Dr. Smith", "Nurse Joy", "Dr. Adams"])
        
print(george.name) 
george.add_employee("Dr. Brown")
print(george.employees) 
        