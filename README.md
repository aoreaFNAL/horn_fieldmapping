# horn_fieldmapping

The code in 'manual_scan_2.py' is the updated version of the code that Adam Watts had for the stand at MI-8. Several 'grammatical' bugs were removed to display properly on the screen and to simplify the text file printout

'AxialTrial.py' is the code used to analyze the data collected from the labview program from pulsing the horn.
It prompts the user to enter the data file (without an extension at the end) and asks for the first and last pulse number of data. It also requires the user to hard code in the array of the number of pulses per location. Since this is done by hand, it is usually 10 or 11, but it is not consistent. A future version of this code will use the data from a different text format and can assume that each location is at 10 pulses per location

'AxialPeak.py' is the equivalent of 'AxialTrial.py', but it takes the max magnetic field measurement at the same index as the current peak. This is when the beam goes through the horn, so it's the magnetic field of interest. However, the former code can be used to determine an estimate on the 'worse case' field that the beam will see.
It prompts the user for the same data as the former code. The analysis is identical other than the peak being taken from a different position.
