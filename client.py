from timeit import default_timer as timer
from dateutil import parser
import threading
import datetime
import socket
import time

def startSendingTime(slave_client):
    while True:
        slave_client.send(str(datetime.datetime.now()).encode())
        print("Recent time sent successfully", end="\n\n")
        time.sleep(5)

def startReceivingTime(slave_client):
    while True:
        synchronized_time = parser.parse(slave_client.recv(1024).decode())
        print("Synchronized time at the client is: " + str(synchronized_time), end="\n\n")

def initiateSlaveClient(port=8080):
    slave_client = socket.socket()
    slave_client.connect(('127.0.0.1', port))
    print("Starting to receive time from server\n")
    threading.Thread(target=startSendingTime, args=(slave_client, )).start()
    print("Starting to receiving synchronized time from server\n")
    threading.Thread(target=startReceivingTime, args=(slave_client, )).start()

if __name__ == '__main__':
    initiateSlaveClient(port=8080)

