import threading
import random
import requests
    
WebPage=int(input('enter a file name'))

RANDOM=10

while True:
    
    def work(WebPage):
        response = requests.get("http://192.168.1.20:5000/file")

            
    
    for i in range(8):
        t2 = threading.Thread(target=work,args=())
    

    
for i in range(8):
    t2 = threading.Thread(target=work,args=())

result=work(num)

t1 = thread = threading(target=work, args=(result) )
t1.start()


