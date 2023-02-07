import pyftdi.spi as spi
import pyftdi.ftdi as ftdi
import pyftdi.gpio as gpio


class LoadCell:
    def __init__(self):
        self.g = gpio.GpioAsyncController()
        self.g.configure('ftdi:///1', direction=0b11111011)
        self.g.set_frequency(100000)
        self.datamask = int(0b00000100)
        compare = self.datamask & self.g.read(peek=True)
        self.g.write(0b00000000)
        self.bitlength=24

    def get_reading(self):
        print("waiting for hx711 rdy...")
        while self.datamask & self.g.read(peek=True):
            pass
            # print(",",end=" ") # Print .... while waiting for reading
        data = 0
        for i in range(self.bitlength+1):
            hi = 0b00001000
            low = 0b00000000
            bytesequence = [hi,low]
            self.g.write(bytesequence) # Write hi then low at frequency so hx711 doesn't go to sleep
            # Read the 24 bits from hx711, bit shift properly
            if(i<24):
                data = data | self.g.read(peek=True) >> 2 << (self.bitlength - 1 - i)

        return LoadCell.twos_comp(data,self.bitlength)

    @staticmethod
    def twos_comp(val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val                         # return positive value as is

if __name__ == "__main__":
    l = LoadCell()
    # from time import sleep
    # while True:
    #     print(l.get_reading())
    #     sleep(0.01)

    f = open("loadcellreadings.txt", "a")

    while True:
        g = input("enter g: ")

        for i in range(100):
            force = l.get_reading()
            f.write("{} g, {} raw \n".format(g, force))
            print("force is = {}".format(force))





    