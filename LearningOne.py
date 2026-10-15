import time


HarryPotter=[]


with open ("HarryPotter.txt", "r") as file:
    content = file.read().split(" ")
    
    for item in content:
        HarryPotter.append(item)
           
print(len(HarryPotter))


        
start = time.time()
mySet=set(HarryPotter)
print(len(mySet))
end = time.time()
length1 = end - start
print("It took", length1, "seconds!")




start = time.time()
myList=list(HarryPotter)
print(len(myList))
end = time.time()
length = end - start
print("It took", length, "seconds!")


HowMuchFaster=length1/length
print("The set is", HowMuchFaster, "times faster than the list!")




