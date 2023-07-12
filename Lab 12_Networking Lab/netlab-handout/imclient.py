#
# A messaging client in Python
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
    if len(sys.argv) != 3:
        print("usage: python3 %s <host> <port>" % sys.argv[0])
        quit(1)
    host = sys.argv[1]
    port = sys.argv[2]

    # TODO 1: open a socket and connect to server
    sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # to create an address, you create a tuple where the first element is the 
    # IP address and the second element is the port
    address = ('', int(port))
    sock_fd.connect(address)

    # message loop
    while(True):
        # TODO 2: send message and receive response
        message_for_server=input('Enter message for server: ')
        sock_fd.send(message_for_server.encode())

        message_received=sock_fd.recv(512).decode()
        print('Received from server: '+message_received)
        

if __name__ == "__main__":
    main()
