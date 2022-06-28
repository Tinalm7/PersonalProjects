#!/usr/local/bin/python3
from socket import *
import sys
import os

#number of bytes to process at once
bufferSize=1024
#server port numberr gotten from command line
serverPort = int(sys.argv[1])
#create server socket
serverSocket = socket (AF_INET, SOCK_STREAM)
serverSocket.bind (('127.0.0.1', serverPort))
#listen for clients trying to connect
serverSocket.listen (1)
print("ready to connect")
while True:
    #connect to client socket
    connectionSocket, addr = serverSocket.accept ()
    #read 1024 bytes from the socket
    initialData = connectionSocket.recv(bufferSize)
    #keep track of amount of file received
    receivedFile=len(initialData)-24
    #size of file as a int
    fileSize=int.from_bytes(initialData[:4], "big")
    #name of file as a string, if file path is in name, it is removed
    fileName=initialData[4:24].strip(b'\0').decode()
    fileName=os.path.basename(fileName)
    #data in file to write to file
    data=initialData[24:]
    with open(fileName, "wb") as file:
        while True:
            # write to the file the bytes we just received
            file.write(data)
            #if all of file received break out of loop
            if receivedFile == fileSize:    
                print("file received")
                break
            # read 1024 bytes from the socket (receive)
            data = connectionSocket.recv(bufferSize)
            receivedFile=receivedFile + len(data)
    connectionSocket.close ()
