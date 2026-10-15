import time
import random
print("press enter as quickly as possible when you see the message 'GO!'")
time.sleep(2)
x=3
while x>0:
    print("game starting in "+str(x)+"...")
    time.sleep(1)
    x=x-1

random_number = random.randint(0, 6)
time.sleep(random_number)
start_time = time.time()
print("GO!")
if input() == "":
    end_time = time.time()
    reaction_time = end_time - start_time
    print("Your reaction time is: " + str(reaction_time) + " seconds.")
