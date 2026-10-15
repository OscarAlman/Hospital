def fileEncryptionTool(file_path):
    text=""
    with open(file_path, 'r') as f:
        for line in f:
            text += line
        
    return encryptionTool(text, file_path)

def encryptionTool(text,file_path):
    encryptedText=""
    shift=int(input("Enter the shift value for encryption (1-25): "))
    for char in text:
        if char.isalpha():
            if char.islower():
                encryptedChar=chr((ord(char)-97+shift)%26+97)
            else:
                encryptedChar=chr((ord(char)-65+shift)%26+65)
            encryptedText+=encryptedChar
        else:
            encryptedText+=char
    return changeFile(encryptedText, file_path)

def changeFile(encryptedText, file_path):
    with open(file_path, 'w') as f:
        f.write(encryptedText)


fileEncryptionTool(file_path=input("Enter the path to the file you want to encrypt: "))
