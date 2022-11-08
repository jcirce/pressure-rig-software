import csv

#class "tube" parameters, name number test
name = "D20K"
number = 1
test = 1

pressure = 1

#file name D20K1_1_1
#name contains tube number, test number, pressure

header = ['pressure[psi]', 'photoname']
data = [
    [1, "{}_{}_{}_{}".format(name, number, test, pressure)]
]

print(data)