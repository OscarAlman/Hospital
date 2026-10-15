
text=input("enter some randome text: ")
characterEntered=input("enter a character to scan for: ")
count=0
for charScanned in text:
    if charScanned.lower()==characterEntered.lower():
        print("found")
        count+=1
total=len(text)
result=count/total
answer=result*100
print("the percentage of the character in the text is: ", answer, "%")
