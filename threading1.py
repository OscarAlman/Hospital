import threading

def helloThread(threadName):
    print("Hello from thread:", threadName)

t1 = threading.Thread(target=helloThread, args=('john',))
t1.start()

t2 = threading.Thread(target=helloThread, args=('bob',))
t2.start()

t3 = threading.Thread(target=helloThread, args=('alice',))
t3.start()
