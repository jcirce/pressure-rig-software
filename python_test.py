def CLI ():

    try:
        tubename = input("enter tube name")
        pressure = float(input("enter pressure[psi]"))
        if(pressure > 30):
            raise Exception

    except Exception as e:
        print(e)
        print("error")


while True:
    CLI()
