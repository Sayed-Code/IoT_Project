import socket
import threading
import sys
import os

#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string
def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break
#------------------------------------------------------------------
def helping():
    print("-----------------------------------\n")
    print("To receive files from the server:\n")
    print("start with command (recv)")
    print("-----------------------------------\n")
    print("To list all the files in the server:\n")
    print("use the command (list)")
    print("-----------------------------------\n")
#------------------------------------------------------------------

#Get host and port
host = input("Host: ")
port = int(input("Port: "))

#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

#Create new thread to wait for data
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()

#Send data to server
#str.encode is used to turn the string message into bytes so it can be sent across the network
while True:
    def find_folder():
        folder = input("Now choose the folder>")
        sock.sendall(str.encode(folder))
        file = open("/home/uniquare/Desktop/project/files_received/"+folder, mode="w", encoding="utf-8") 
        RecvData = sock.recv(1024)
        file.write(str(RecvData.decode("utf-8")))
        file.close()

#Define the input provided by the user
    cmd = input("input_command>")
   
    if cmd == "recv":
        specify = input("Choose a file after listing using the command (list)>")
        if specify == "list":
            print(os.listdir("/home/uniquare/Desktop/project/files_to_send"))
            find_folder()

            choice = input("do you want to recv another file? (y/n)")
            if choice == "y":
                find_folder()
                
        else:
            print("command not recognized")
    elif cmd == "list":
        print(os.listdir("/home/uniquare/Desktop/project/files_to_send"))
    elif cmd == "quit":
        sys.exit(0)
#If the user did not use our command line before she/he can type "help" that provide some description
    elif cmd == "help":
        helping()
    else:
        print("command not recognized")