class Hospital:
    def __init__(self,name,employees=[]):   # innit is a short hand for initialize, it is a constructor method that is called when an object is created. It takes in the name of the hospital and a list of employees as parameters. The list of employees is optional and defaults to an empty list if not provided.
        self.name=name                      # you cant have mul
        self.employees=[]
    
    def add_employee(self,employee):
        """
        Adds an employee to the hospital.
        """
        self.employees.append(employee)
    def count_employees(self):
        """
        Returns the count of employees in the hospital.
        """
        countOfEmps = len(self.employees)
        return countOfEmps
    def count_doctors(self):
        countOfDocs = 0
        #counts the number of doctors in the hospital by iterating through the list of employees and checking if each employee is an instance of the Doctor class. If it is, it increments the countOfDocs variable by 1. Finally, it returns the countOfDocs variable.
        for employee in self.employees:
            if isinstance(employee, Doctor):
                countOfDocs += 1
        return countOfDocs
    def count_nurses(self):
        """
        Returns the count of nurses in the hospital.
        """
        countOfNurses = 0
        for employee in self.employees:
            if isinstance(employee, Nurse):
                countOfNurses += 1
        return countOfNurses
    
    def print_doctors(self):
        '''
        Prints the names of all doctors in the hospital.'''
        for employee in self.employees:
            if isinstance(employee, Doctor):
                print(employee.name)
    
    def print_nurses(self):
        '''
        Prints the names of all nurses in the hospital.'''
        for employee in self.employees:
            if isinstance(employee, Nurse):
                print(employee.name)
    
    
        
    def search_for_doctor(self, name):
        '''
        Searches for a doctor by name.

        The name of the doctor to search for.

        The doctor object if found, otherwise None.
        '''
        for employee in self.employees:
            if isinstance(employee, Doctor) and employee.name.lower() == name.lower():
                return employee
        return None
   

##################################################################################
##################################################################################
class Employee:
    def __init__(self,parameterName,age):
        self.name=parameterName
        self.age=age

class Doctor(Employee):
    '''
    A class representing a doctor, which is a subclass of Employee.
    this is clear as employee is in the brackets, this means that doctor is a subclass of employee, and inherits all the methods and attributes of the employee class.
    '''
    def __init__(self,parameterName,parameterSpecialty,age):
        '''
        Initializes a Doctor object with a name and specialty.'''
        super().__init__(parameterName,age)
        self.specialty=parameterSpecialty
    
    def __str__(self):
        return f"Dr Name: {self.name}, Specialty: {self.specialty}, Age: {self.age}"

class Nurse(Employee):
    '''A class representing a nurse which is a subclass of Employee'''
    def __init__(self,parameterName,age):
        '''Initializes a Nurse object with a name.'''
        super().__init__(parameterName,age)

    def __str__(self):
        return f"Nurse Name: {self.name}, Age: {self.age}"

myHospital=Hospital("St Georges Hospital", []) #this is the hospital object, it has a name and a list of employees. The list of employees is empty at the moment.
                                               #its also an instance of the Hospital class, so it has all the methods of the Hospital class.

katie=Nurse('Katie', 25) #this is a nurse object, it has a name and is an instance of the Nurse class, which is a subclass of the Employee class.
alice=Nurse('Alice', 30) #this is a nurse object, it has a name and is an instance of the Nurse class, which is a subclass of the Employee class.   
john=Doctor('John','Heart', 40) #this is a doctor object, it has a name and a specialty and is an instance of the Doctor class, which is a subclass of the Employee class.
david=Doctor('David','Neuro', 35) #this is a doctor object, it has a name and a specialty and is an instance of the Doctor class, which is a subclass of the Employee class.
bob=Employee('Bob', 28) #this is a nurse object, it has a name and is an instance of the Nurse class, which is a subclass of the Employee class.
malachi=Employee('Malachi', 32) #this is a nurse object
william=Employee('William', 26) #this is a nurse object
charlotte=Employee('Charlotte', 29) #this is a nurse object
myHospital.add_employee(charlotte) #this is calling the add_employee method of the Hospital class, and passing in the nurse object as an argument. This will add the nurse to the list of employees in the hospital.
myHospital.add_employee(katie) #this is calling the add_employee method of the Hospital class, and passing in the nurse object as an argument. This will add the nurse to the list of employees in the hospital.
myHospital.add_employee(alice) #this is calling the add_employee method of the Hospital class, and passing in the nurse object as an argument. This will add the nurse to the list of employees in the hospital.
myHospital.add_employee(john) #this is calling the add_employee method of the Hospital class, and passing in the doctor object as an argument. This will add the doctor to the list of employees in the hospital.  
myHospital.add_employee(david) #this is calling the add_employee method of the Hospital class, and passing in the doctor object as an argument. This will add the doctor to the list of employees in the hospital.
myHospital.add_employee(bob) #this is calling the add_employee method of the Hospital class, and passing in the employee object as an argument. This will add the employee to the list of employees in the hospital.
myHospital.add_employee(malachi) #this is calling the add_employee method of the Hospital class, and passing in the employee object as an argument. This will add the employee to the list of employees inthe hospital.
myHospital.add_employee(william) #this is calling the add_employee method of the Hospital class, and passing in the employee object as an argument. This will add the employee to the list of employees inthe hospital.


print(john)
print(alice)



print(myHospital.count_employees()) 

#this is printing the list of employees in the hospital. It will print the memory address of the objects, not the names of the employees. This is because we have not defined a __str__ method for the Employee class. We will do that next.
doctor=input("Enter the name of the doctor you want to search for: ") #this is asking the user to enter the name of the doctor they want to search for. It will store the input in the variable doctor.
found_doctor=myHospital.search_for_doctor(doctor) #this is calling the search_for_doctor method of the Hospital class, and passing in the name of the doctor as an argument.
if found_doctor is not None: #this is checking if the doctor was found. If it was found, it will print the name and specialty of the doctor. If it was not found, it will print "Doctor not found."
    print('doctor has been found, his name is',found_doctor.name,'and his specialty is',found_doctor.specialty)
else:
    print('Doctor not found.')
#TODO 👍 Create another subclass for Nurse
#TOTO add age to the base class , as both burses and Drs have age
#TODO 🥳 Add a function at the hostpital class, to return the count of employees
#TODO 🥳 Add a function at the hostpital class, to return the count of Drs
#TODO 🥳 Add a function at the hostpital class, to return the count of Nurses
#TODO 🥳 Add a function at the hostpital class, to print Drs only
#TODO 🥳 Add a function at the hostpital class, to print Nurses only
#TODO 🥳 search for a doctor by name. The search should ignore capitals (“smith” matches “Smith”), only match doctors, and give back the doctor if found or None if not.
#TODO 🥳 Every method needs a docstring explaining what it does.
#TODO 🥳 use __str__ so when you do print(drDave) it prints something human readable
#TODO .... for extra points use  __repr__   so when you print(employees)  it prints somethings useful





