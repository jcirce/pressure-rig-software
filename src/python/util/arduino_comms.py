import serial
from threading import Thread
from queue import Queue
# from multiprocessing import Process, Manager, Queue
import time

class CommsController():
    def __init__(self):
        self.serialThread = Thread(target=self.handle_comms)
        # self.process = Process(target=self.handle_comms)
        self.commandList = Queue() # List of commands to send to arduino
        self.responseList = Queue() # List of responses from arduino
        self.arduinoConnected = False

        try:
            # If windows changes arduino com port need to adjust port here
            self.ser = serial.Serial(port='COM3', \
                baudrate=115200, parity=serial.PARITY_NONE, \
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, \
                        timeout = 10)
            self.arduinoConnected = True

        except:
            print("Couldn't connect to Arduino")

        self.serialThread.start() # Start serial comms thread

    def handle_comms(self):
        while(1):
            try:
                if not self.commandList.empty():
                    if self.arduinoConnected:
                        self.ser.write(self.commandList.get()) # Send last command
                        time.sleep(0.1) # hard wait to let arduino respond
                    if self.ser.inWaiting() > 0: # if bytes avail in serial port, read them
                        self.readLine()
            except Exception as e:
                print(e)

    def append_command(self, command_string: str):
        self.commandList.put(command_string)

    def readLine(self):
        if self.arduinoConnected:
            line = self.ser.read_until(expected=b"\n\r") # Read line until the \n\r chars
            self.responseList.put(line) # put this line into the responseList

    def checkConnection(self):
        pass

if __name__ == "__main__":
    c = CommsController()

    #i=255 #pressure = 0

    while True:
        time.sleep(0.5)
        c.append_command(b"R0%\n") #need "b" as part of string, interpret as raw bytes

        bit = float((input("enter 0-255 bit")))
     
        s = f"S1,A{bit}%\n" #puts variable into command string

        c.append_command(bytes(s, 'UTF-8'))# Interpret stringas bytes from utf-8 format

        while not c.responseList.empty():
            a=c.responseList.get()
            print(a)

