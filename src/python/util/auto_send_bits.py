from arduino_comms import CommsController
import time 
import numpy as np 

if __name__ == "__main__":
    c = CommsController()

    #need an array here 
    val1    = 45 #10.2 psi 
    val2    = 30 #13.4 psi
    array   = [val1,val2]
    bit_array = np.array([255,    88,   61,   41,   30,   22,   20,   18,   16,   14,   12,   11,   10,     9,     6,     4]) 
    # psi = np.array([1.7,   3.3,  4.4,  5.9,  7.2,  8.7,  9.2,  9.7, 10.3, 10.9, 11.6, 12.0, 12.5,  13.0,  14.7,  16.0,  17.7,  18.8, 19.9])

#for j in range(5):
    for i in range(len(bit_array)): 
        print(i)
        time.sleep(0.9)
        c.append_command(b"R0%\n") #need "b" as part of string, interpret as raw bytes
        bit = float((bit_array[i]))
        s = f"S1,A{bit}%\n" #puts variable into command string
        c.append_command(bytes(s, 'UTF-8'))# Interpret stringas bytes from utf-8 format
        print(s)

        while not c.responseList.empty():
            a=c.responseList.get()
            print(a)
            