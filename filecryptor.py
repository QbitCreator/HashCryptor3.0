import hashcrypt as hc

from tkinter import Tk
from tkinter.filedialog import askopenfilename

input("Press ENTER to select a file:")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename, "selected.")
file = open(filename, "rb")
option=input("ENCRYPT(e) or DECRYPT(d)?")
data=file.read()
file.close()
if option=="e":
    password=input("You selected ENCRYPTION.\nChoose a PASSWORD:")
    if input("Are you sure?(y/n)")!="y":
        exit()
    cipherdata=hc.encrypt(data,password)
    file = open(filename, "wb")
    file.write(cipherdata)
    
elif option=="d":
    password=input("You selected DECRYPTION.\nWhat's the PASSWORD?:")
    if input("Are you sure?(y/n)")!="y":
        exit()
    cipherdata=hc.decrypt(data,password)
    if cipherdata!=-1:
        file = open(filename, "wb")
        file.write(cipherdata)
    else:
        print("Password wrong!")
    
    
    
    
    
