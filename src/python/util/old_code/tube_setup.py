import numpy as np
import os



class Tube:
    def __init__(self, name, number, test):
        self.name = name
        self.number = number
        self.test = test

    def __str__(self):
        return f"{self.name}{self.number}_{self.test}"

def CLI_init ():

    try:
        name = input("enter tube name (ex: D20K or S45M)")
        number = input("enter tube number")
        test = input("enter test number")

        tube = Tube(name, number, test)
        return tube
        
    except:
        print("error init")

def CLI ():

    try:
        pressure = float(input("enter pressure[psi]"))
        print(convert2pottake2(pressure))

        if(pressure < 2 or pressure > 29):
            raise Exception

    

    except Exception as e:
        print(e)
        print("error")



def convert2potinput (psi_des):

    pot_exact = 0.001*(psi_des**6)  -0.0406*(psi_des**5) + 0.8780*(psi_des**4) -10.9641*(psi_des**3) + 80.0224*(psi_des**2) -328.3181*psi_des +  660.14
    pot_input = round(pot_exact)

    return pot_input

def convert2pottake2 (psi_d):
    pot_exact =  0.0001*(psi_d**6)  -0.0087*(psi_d**5)  +  0.2942*(psi_d**4)   -5.1036*(psi_d**3) +  48.1897*(psi_d**2) -243.1506*psi_d +  574.9430


tube = CLI_init()



#while True:
parent_dir = "/Users/student/desktop/pressure-rig-software/src/python/util"

dir = str(tube)

path = os.path.join(parent_dir, dir)

os.mkdir(path)
 


