# Tube Testing Procedure
## _Soft Robotics Thesis_

> this procedure is a work in progress, 
> please ask questions if something is unclear
> last updated 12/2/22

## 1. Plug tube in

1. unplug hex mount from black pipe
2. fasten mount to fastener in the tube
3. plug hex mount in
4. make sure tube stands up on black wall

## 2. Prep Rig

1. untwist E-stop
2. plug in arduino
3. reset arduino until tank is pressurized

## 3. Run test.py software

1. open command window on computer (open terminal)
2. go to directory that test.py is in
''' sh
cd desktop/pressure-rig-software/src/python/util
'''
3. run script 
''' sh
python test.py
'''
4. script will prompt tube name, number, and test number
> if mistake/typo is made, end program
> skip to _clean up dir_ section

5. Start Test
Once camera in focus, use keyboard for commands
- press _space bar_ to increase pressure
- press _m_ key to take photo

**NOTE:**
Camera will not take commands unless you are clicked on the frame's view on the computer, ensure you are not typing in the terminal, but clicked on the camera frame

6. Clean up dir
- use file viewer to see that all the images are in correct directory and labelled properly (relabel as needed)
- remove any dir/folders created with typos
- 

## 4. Push Photos to github












-for each tube

-for each change in pressure
- take a photo
- take flex sensor reading
- take force sensor reading

- label photos with tube name and current pressure
- store pressure, flex sensor resistance, force sensor reading in .csv labelled for current tube

- to change pressure increment, manually adjust potentiometer 
startup checks
	- arduino connected
	- camera connected



command line interface
- 1. enter tube name
- (adjust pot)
- 2. enter pressure value
- 3. collect data y/n?
	-no, go back to 2
	- print data to terminal
- 4. data good?
	- yes, append .csv, 
	- no go back to 2
- 5. new pressure or new tube?
	new pressure -> 2
	new tube -> 1 

arduino tasks
	- measure flex sensor resistance
	- measure force sensor (unit?)
	- measure resovoir pressure
		- keep resovoir above 25 psi, below 29 psi
	- accept commands from serial port
	- send data over serial port

arduino saftey tasks
	- check pressure increase on "pump on" signal
		- if error, put arduino to error state
		(pressure valve could be disconnected or sensor broken or theres a leak somewhere)
	- check for errors (add leds?)

arduino command library
	- record data and send data back to computer
	- start
	- stop
	- adjust resovoir pressure range
	- [future: control pressure regulator pressure]
	- software e-stop 
	- dump errors on serial monitor
	- handshake

arduino error names
	- pumping error (t/f)



directory hierarchy
- tube-data
	- tube-name
		- photos
		- tube-data.csv
		 

list of components to still buy
	- force sensor
	- blow off valve for 45? psi
	- differential ADC (13 bit minimum)
	- perf board
	- digital potentiometer
	- e-stop button

csv structure
- tube name, pressure, data1, data2, ..., photo-file-name.png