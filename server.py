from dateutil import parser
import threading
import datetime
import socket
import time

client_data = {}

def startReceivingClockTime(connector, address):
    while True:
        clock_time_string = connector.recv(1024).decode()
        clock_time = parser.parse(clock_time_string)
        clock_time_diff = datetime.datetime.now() - clock_time
        client_data[address] = {"clock_time": clock_time, "time_difference": clock_time_diff, "connector": connector}
        print(f"Client Data updated with: {address}\n")
        time.sleep(5)

def startConnecting(master_server):
    while True:
        master_slave_connector, addr = master_server.accept()
        slave_address = f"{addr[0]}:{addr[1]}"
        print(f"{slave_address} got connected successfully")
        threading.Thread(target=startReceivingClockTime, args=(master_slave_connector, slave_address)).start()

def getAverageClockDiff():
    time_difference_list = [client['time_difference'] for client in client_data.values()]
    sum_of_clock_difference = sum(time_difference_list, datetime.timedelta(0, 0))
    return sum_of_clock_difference / len(client_data) if client_data else datetime.timedelta(0, 0)

def synchronizeAllClocks():
    while True:
        print("New synchronization cycle started.")
        print(f"Number of clients to be synchronized: {len(client_data)}")
        average_clock_difference = getAverageClockDiff()
        for client in client_data.values():
            try:
                synchronized_time = datetime.datetime.now() + average_clock_difference
                client['connector'].send(str(synchronized_time).encode())
            except Exception as e:
                print(f"Something went wrong while sending synchronized time through {client['connector'].getpeername()}")

        print("\n\n")
        time.sleep(5)

def initiateClockServer(port=8080):
    master_server = socket.socket()
S    master_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket at master node created successfully\n")
    master_server.bind(('', port))
    master_server.listen(10)
    print("Clock server started...\n")
    print("Starting to make connections...\n")
    threading.Thread(target=startConnecting, args=(master_server,)).start()
    print("Starting synchronization parallelly...\n")
    threading.Thread(target=synchronizeAllClocks, args=()).start()

if __name__ == '__main__':
    initiateClockServer(port=8080)

