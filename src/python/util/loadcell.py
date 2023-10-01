import pyftdi.spi as spi
import pyftdi.ftdi as ftdi
import pyftdi.gpio as gpio


class LoadCell:
    # DAT to AD2
    # CLK to AD3

    #second load cell
    # DAT to AD4
    # CLK to AD5

    def __init__(self):
        self.g = gpio.GpioAsyncController()
        self.g.configure('ftdi:///1', direction=0b11101011) # ad2 and 4 inputs
        self.g.set_frequency(100000)
        self.datamask =  int(0b00000100) #ad2 -> 3rd bit
        self.datamask2 = int(0b00010000) #ad4-> 5th bit
        compare = self.datamask & self.g.read(peek=True)
        self.g.write(0b00000000)
        self.bitlength=24

    def get_reading(self):
        #print("waiting for hx711 rdy...")
        while self.datamask & self.g.read(peek=True):
            pass
            # print(",",end=" ") # Print .... while waiting for reading
        data = 0
        for i in range(self.bitlength+1):
            hi = 0b00001000 #ad3-> 4th bit
            low = 0b00000000
            bytesequence = [hi,low]
            self.g.write(bytesequence) # Write hi then low at frequency so hx711 doesn't go to sleep
            # Read the 24 bits from hx711, bit shift properly
            if(i<24):
                data = data | self.g.read(peek=True) >> 2 << (self.bitlength - 1 - i) 

        return LoadCell.twos_comp(data,self.bitlength)
    
    #for the second load cell
    def get_reading2(self):
        #print("waiting for hx711 rdy...")
        while self.datamask2 & self.g.read(peek=True):
            pass
            # print(",",end=" ") # Print .... while waiting for reading
        data = 0
        for i in range(self.bitlength+1):
            hi = 0b00100000 #ad5 -> 6th bit
            low = 0b00000000 
            bytesequence = [hi,low]
            self.g.write(bytesequence) # Write hi then low at frequency so hx711 doesn't go to sleep
            # Read the 24 bits from hx711, bit shift properly
            if(i<24):
                data = data | self.g.read(peek=True) >> 4 << (self.bitlength - 1 - i) #try shift 4 first perhspapspspsp

        return LoadCell.twos_comp(data,self.bitlength)
    

    @staticmethod
    def twos_comp(val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val                         # return positive value as is

if __name__ == "__main__":
    l = LoadCell()
    from time import sleep
    # while True:
    #     print(l.get_reading())
    #     sleep(0.01)

    f = open("loadcellreadings.txt", "a")

    # while True:
    g = input("enter g: ") # g is for grams applied

    for i in range(100):
        forcey = l.get_reading()
        forcex = l.get_reading2()

        if forcex < 30000000 and forcey < 30000000:
            f.write("{}, {}\n".format(g, forcex))
            print("raw is = {} in x and {} in y".format(forcex, forcey))
        
    f.close()

    
    
        

        





    