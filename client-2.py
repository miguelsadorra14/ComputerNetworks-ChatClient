# create new socket using socket function
# used to initiate or respond to a connection request
import socket
import threading
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

buffer = 1
host = "143.47.184.219"
port = 5378

# establish a connection using a socket
host_port = (host, port)
sock.connect(host_port)

while True:
        # input unique username
        input1 = input("Login with a username: ")

        if input1 == "!quit":
            print("You have exited the program.")
            exit()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(host_port)

        sock.sendall(b"HELLO-FROM " + input1.encode("utf-8") + b"\n")
        data = ''
        dataTemp = ''
        while True:
            dataTemp = sock.recv(buffer).decode('utf-8')
            data = data + dataTemp

            if '\n' not in data:
                continue
            else:
                break

        if data == "IN-USE\n":
            print("----- Username is already taken -----")

        elif data == "BUSY\n":
            print('----- Server is currently busy ------')

        else:
            print(data)
            break

# listen for incoming messages
def inbox():
    while True:
        try:
            data = ''
            dataTemp = ''
            while True:
                dataTemp = sock.recv(buffer).decode('utf-8')
                data = data + dataTemp

                if '\n' not in data:
                    continue
                else:
                    break

            if data != b'':
                header = data
                header = header.split()[0]
                
                if header == "SEND-OK":
                    print("----- Message delivered successfully -----")
                    continue
                
                if header == "DELIVERY":
                    data = data.replace("DELIVERY", '')
                    userHandle = data.split()[0]
                    data = data.replace(userHandle + ' ', '')
                    data = userHandle + ':' + data
                    print("\n" + data)
                    continue
                
                if header == "BAD-RQST-BODY":
                    print("----- Please input message -----")
                    continue
                
                if header == "BAD-RQST-HDR":
                    print("----- Wrong header -----")
                    continue
                if header == "WHO-OK":
                    data = data.replace("WHO-OK ", '')
                    print(data)
                
                else:
                    print("\n" + data)
                    continue
            else:
                continue
            
        except OSError as msg1:
            print(msg1)
            sock.close()
            break

# write to terminal and send to server
def sendMessage():
    while True:
        try:
            input2 = input()
            if input2 == "!quit":
                print("You have exited the program.")
                os._exit(os.EX_OK)
                
            if input2 == "!who":
                sock.sendall(b"WHO\n")
                print("----- online members -----")
                continue
                
            if "@" in input2:
                username = input2.split()[0]
                username = username.replace("@", '')
                username2 = username
                message = input2
                if username in message:
                    message = message.replace("@" + username, '')
                username2 = username2.encode("utf-8")
                message = message.encode("utf-8")
                sock.sendall(b"SEND " + username2 + b" " + message + b"\n")
                continue
            else:
                sock.sendall(input2.encode('utf-8')+ b'\n')

        except OSError as msg:
            print(msg)


def main():
    sendMessage_thread = threading.Thread(target=sendMessage)
    inbox_thread = threading.Thread(target=inbox)
    inbox_thread.daemon = True


    sendMessage_thread.start()
    inbox_thread.start()

main()