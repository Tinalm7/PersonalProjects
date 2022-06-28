#!/usr/local/bin/python3
from socket import *
import sys
import os

#amount of data to read from file and send
bufferSize=1000
#server IP gotten from command line
serverIP = sys.argv[1]
#server port gotten from commandline
serverPort = int(sys.argv[2])
#creat client socket
clientSocket = socket (AF_INET, SOCK_STREAM)
#connect to server socket
clientSocket.connect ((serverIP, serverPort ))
print("connected to socket")
#get fileName from command line, also convert to 20 bytes 
fileName = sys.argv[3]
fileNameData=fileName.encode().rjust(20, b'\0')
#get size of file in 4 bytes
fileSize = os.path.getsize(fileName).to_bytes(4, "big")
#open file to be read as a binary file
with open(fileName, 'rb') as file:
    #read initial data
    initialData=file.read(bufferSize)
    #create byte array of fileSize, fileNameData, data and send it
    data=bytearray(fileSize)
    data.extend(fileNameData)
    data.extend(initialData)
    clientSocket.send(data)
    while True:
        #read binary data from file
        data = file.read(bufferSize)
        #if there is no more data in file break loop
        if(len(data) == 0):
            print("file sent")
            break
        #send data to server
        clientSocket.send (data)
#close client socket
clientSocket.close ()