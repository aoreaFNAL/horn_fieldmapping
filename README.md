# horn_fieldmapping

The code in 'manual_scan_2.py' is the updated version of the code that Adam Watts had for the stand at MI-8. Several 'grammatical' bugs were removed to display properly on the screen and to simplify the text file printout

'AxialTrial.py' is the code used to analyze the data collected from the labview program from pulsing the horn.
It prompts the user to enter the data file (without an extension at the end) and asks for the first and last pulse number of data. It also requires the user to hard code in the array of the number of pulses per location. Since this is done by hand, it is usually 10 or 11, but it is not consistent. A future version of this code will use the data from a different text format and can assume that each location is at 10 pulses per location

'AxialPeak.py' is the equivalent of 'AxialTrial.py', but it takes the max magnetic field measurement at the same index as the current peak. This is when the beam goes through the horn, so it's the magnetic field of interest. However, the former code can be used to determine an estimate on the 'worse case' field that the beam will see.
It prompts the user for the same data as the former code. The analysis is identical other than the peak being taken from a different position.

'BackgroundRemoval.py' works with the same code as 'AxialTrial.py', but with a set bench of background data being subtracted from each data array. It reduced the data too much, so I stuck with averaging the signal rather than doing a pedestal subtraction to avoid deleting valuable data.

'FFT_Background.py' was created to analyze the data taken and see if there was a difference between the FFT of the data and background. It turned out that the same frequencies were seen, but with lower magnitudes, than the data so the signal averaging approach was taken since the noise appears to be random rather than stuck on a low or high pass filter cutoff

'NoiseAnalysis.py' was a quick script to read the data from the RampUp.xls sheet and verify that the data is different from just noise. I saw a distinct spike at the start of the current ramp up which points to the data being a real signal.

'TrialNoise.py' is a quick analysis to test out the signal averaging by increasing the number of iterations from 10 to 100. I also plotted the background data in the back to veryfy that we were reading somthing other than just noise. This works with the AllPlanes.xlxs sheet

'Averaging.py' is idential to 'AxialPeak.py' but it uses the mean function with the axis option and plots the standard +/- error band over the plots. It produces the same data but in a slightly more efficient manner since it uses the built in function and also has that fine band that gives the user a sense of how reliable the data is
