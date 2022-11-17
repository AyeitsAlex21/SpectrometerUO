READ ME FILE FOR HR460.py

Created by: Justin deMattos MIIP Optics Track �20

Designed for: Control of Jobin-Yvon Spex HR460 Spectrometer in APL

OS and PYTHON VERSION:

Project done on Ubuntu 22.04.1 LTS and Python 3.7.15

SETUP:

Spectrometer needs to be connected to DataScan unit, which then connects to the computer via a USB port. NOTE: Adapters needed to go from serial port to USB!

Once connected, the USB port name needs to be found. This can be done by following steps outlined in the manual given in this folder.

Run "sudo chmod a+rw /dev/ttyUSB0" (replace 'ttyUSB0' with USB file the spectrometer got assigned to) to give the code permission to read into the file descriptor stored for the USB file.

Then run the source command (source [script path]) on the activate script located at oldEnv/bin/activate to enter the python environment.
Note: if successfull then you should see "(oldEnv)" at the far left of the terminal.

The program can then be started by navigating to this directory in a terminal and running �python3 HR460.py�. NOTE: I have not tried running the code in normal Python (python HR460.py), 
but I do not think it will work because the code was designed for Python 3 use, which is the most up-to-date version of Python.

Once the program is started, it will prompt the user, in the command line, for the name of the USB port associated with the spectrometer input. For reference, the USB port that it was connected to when I was using it was �ttyUSB0�

NOTE: If packages are not installed run "pip install -r requirements.txt" in the folder that it is located inside.

FUNCTIONALITY:

If the correct USB port was entered, the GUI will display with an �Initialize� button in the very center. To start up the device, click the button and the spectrometer will begin its initialization process. 
POSSIBLE PROBLEM: Sometimes the device will not initialize correctly and will error out. If this happens, restart the spectrometer and the code by physically turning the spectrometer off for a few seconds and then rerun the code!

The user will then be presented with the main menu options: Information, Scanning, and Tool Control

INFORMATION MENU: The information menu explains how the device works, the physics behind it, and information needed to run scans and work the device. 
NOTE: As of mid-December 2019, this menu is NOT fully functional

SCANNING MENU: The scanning menu is used to take scans on input sources. Use the slider bars, input fields, and drop-down menus to select the parameters that fit your scan and select the �Start Scan� button to begin. If something was entered incorrectly or the input wasn�t valid in any way, an error will be displayed below the start button in bold red text. 

If all parameters are cleared, red text and loading bar will be displayed where the error message would be and the text will inform the user of the progress on the scan. 

Once a scan is completed, a new plot will replace the sample plot, showing the data collected. This can then be downloaded as a .csv, .png, or .jpg file using the buttons below the plot. Plot options can also be changed using the Plot Options menu button below the plot. 
NOTE: The scatter plot option does not work as of mid-December 2019. The plot will still work if the option is selected but it will not actually be a scatter plot. It will remain a line plot with the lines between the points interpolated.
NOTE2: As of mid-December 2019, the user cannot change the names of the axes on the plot. This is something we hope to have fixed in the future.

TOOL OPTIONS MENU: This menu is meant to be for individual control of mechanisms within the spectrometer. Sliders, input fields, and drop down menus will allow for user control of the device. For example, if calibration is needed to be completed, the grating may need to be moved to a certain position and not scanned across. The tool options menu will allow you to move the motor to a certain position. 
NOTE: As of mid-December 2019 this menu has not been completed!


HELP:

For more information or help, please refer to the 3 manuals in this folder: 

UserManual: The user manual for the spectrometer from the company

InterfaceManual: The interfacing manual for the spectrometer from the company

Handbook: A manual written by Justin deMattos describing the physics and technical details

For more information, please see Dr. Bryan Boggs.


