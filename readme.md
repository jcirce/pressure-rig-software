# Tube Testing Procedure
## _Soft Robotics Thesis_

> this procedure is a work in progress, 
> please ask questions if something is unclear
> last updated 12/2/22

## 1. Plug tube in

1. unplug old tube or the white tube loop
2. screw on attachment in the tube to the male threaded end
*make sure tight with pliers
4. make sure tube stands up on black wall

## 2. Prep Rig

1. untwist E-stop (until regulator turns on)
2. plug in arduino with gray cord
3. reset arduino until tank is pressurized (little red putton left of plug)

##if there is a leak
- you will probably hear it in one of two ways, either a stream of air coming out from somewhere, or the regulator will not stop making noise (its a very repetitive honking noise)
- use bubble sauce with a toothpick to identify where the leak is coming from
- check connections, starting with tube to the metal barb
- once the source of the leak is found, press E-stop and fix the problem. 

## 3. Run test.py software

1. open command prompt on computer (open terminal)
2. go to directory that test.py is in
``` sh
cd desktop/pressure-rig-software/src/python/util
```
3. run script 
``` sh
python test.py
```
4. script will prompt tube name, number, and test number
> if mistake/typo is made, 
> end program (control c)
> skip to _clean up dir_ section

**NOTE:**
Camera will not take commands unless you are clicked on the frame's view on the computer, ensure you are not typing in the terminal, but clicked on the camera frame

5. Start Test (click on camera window)
Once camera in focus, and tube has settled, use keyboard for commands
- press _space bar_ to increase pressure
- press _m_ key to take photo

6. After Test: 
> 1. Reset arduino to release pressure
> 2. Press E-stop

7. Clean up dir (if needed)
- use file explorer (got to desktop/pressure-rig-software/data) to see that all the images are labelled properly (relabel as needed)
- remove any dir/folders created with typos

## 4. Push Photos to github
1. close file viewer, open terminal, cd into pressure-rig-software
```
cd desktop/pressure-rig-software
```
2. git pull to make sure everything is up to data
```
git pull origin devel
```
3. check status of all the new files
```
git status
```
4. you should see "untracked files", these will be the new folders with the new photos added (dont want to add each photo individually, just add the whole folder)
```
git add data/D20K4_1 
```
5. check status again (if unsure) 
photos should show up as green, under "changes to be committed"
```
git status
```
6. add commit message 
```
git commit -m "jeannette adding photos"
```
7. push photos to github
```
git push origin devel
```
8. should see updated on github page
