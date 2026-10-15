myInput=input('give me a long bit of text please')

def makeFile(myInput):
    with open('file.txt','w') as f:
       f.write(myInput)
   
    with open('file.txt','r') as f:
        content=f.read()
   
    numOfChar=len(content)
    return numOfChar
result=makeFile(myInput)

def askForChar():
    character=input('give me a character to scan for')
    return character  

resultCharacter=askForChar()

def scanForChar(resultCharacter):
    with open('file.txt','r') as f:
        content=f.read()
   
    count=0
    for charScanned in content:
        if charScanned == resultCharacter:
            count+=1
    return count

def calculatePercentage(count, numOfChar):
    percentage=(count/numOfChar)*100
    return percentage

calculatPercentage=calculatePercentage(scanForChar(resultCharacter), result)
print('the percentage of the character in the text is: ', calculatPercentage, '%')
   
