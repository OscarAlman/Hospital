NumberEntered=int(input("Enter a number: "))
num1 = NumberEntered

mylist=[]
zero=False
while zero==False: 
    if NumberEntered==1:
       mylist=[1]
       zero=True
       
 
    num1=num1//2
    remainder=num1%2
    mylist.append(remainder)
    
    if num1==0:
        zero=True
    
    





mylist.reverse()
print(mylist)