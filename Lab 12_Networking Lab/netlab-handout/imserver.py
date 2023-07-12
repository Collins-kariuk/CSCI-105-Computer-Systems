#
# A messaging server in Python
#
# Name 1: Collins Kariuki
#
# Name 2: Joram Amador
#
#

import sys
import socket
from os import _exit as quit

def main():
    # parse arguments
    if len(sys.argv) != 2:
        print("usage: python3 %s <port>" % sys.argv[0])
        quit(1)
    port = sys.argv[1]
    
    # TODO 1: open a socket, bind, and listen
    sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # to create an address, you create a tuple where the first element is the 
    # IP address and the second element is the port
    address = ('', int(port))
    sock_fd.bind(address)
    sock_fd.listen(1)
    
    # TODO 2: accept connections from client
    conn,addr=sock_fd.accept()

    # message loop
    while(True):
        # TODO 3: receive a message from client and send response

        # this is the message received from client
        # we use decode to convert bytes to string object
        message_received=conn.recv(512).decode()
        print('Received from client: '+message_received)
        # the message to send to the client
        message_to_send=input('Enter message for client: ')
        # sending the message to the client
        # use encode to convert strings to bytes
        conn.send(message_to_send.encode())


if __name__ == "__main__":
    main()
