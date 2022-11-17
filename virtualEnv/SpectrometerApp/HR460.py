#Code written by Justin deMattos (MIIP Optics Track '20)
#Designed for use with Jobin Yvon-Spex HR460 Spectrometer
#Advanced Project Lab University of Oregon
#Function: Creates the graphical user interface to run and operate spectrometer

#Multiple packages needed:
import tkinter as tk
import csv
import time
import math
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk
from PIL import Image
#from test import test
from Spectrometer import Spectrometer
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


#Prompt the user for the name of the USB port to communicate with
usb = input("Enter the USB port name for the Spectrometer: ")

class HR460App(tk.Tk):

    def __init__(self, *args, **kwargs):

        #Create tkinter window container
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Defined this as a global to manage window size in other classes
        global window

        window=self

        #Don't allow user to change the size of the window (stretches things out and makes it messy)
        self.resizable(width=False,height=False)

        #Create a frames dictionary and set the title of the app
        self.frames = {}
        self.title("Jobin-Yvon HR460")

        #Create the different window frames. Add other windows here!
        for F in (StartPage, MainMenu, Information, Scanning, Tools):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        #Show the start page first
        self.show_frame(StartPage)

    #Function used to show the window requested
    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()

#Our start page class
class StartPage(tk.Frame):

    def __init__(self,parent,controller):
        self.controller = controller
        imageName = 'Slide1.jpeg'

        #Set specific window size. Can change if needed but will throw off placement
        w = 900
        h = 507
        tk.Frame.__init__(self,parent)
        
        #Create a canvas on the window to store the background image and pack it into the window
        self.canvas = tk.Canvas(self, width=w, height=h)
        self.image = ImageTk.PhotoImage(file=imageName)
        self.canvas.create_image(0,0,image=self.image,anchor='nw')
        self.canvas.pack()

        #Create the opening initialize button
        self.buttonFont = ("jua",15,'bold')
        self.init_button = tk.Button(self, text = "Initialize", command = self.initializeButton, anchor = 'center', width = 20, activebackground = '#ffffff')
        self.init_button.config(font=self.buttonFont)
        
        #Note: because of the way pack() works, I had to create a window over the original window to store the button
        self.init_button_window = self.canvas.create_window(w/2,0.35*h,anchor='center',window=self.init_button)
    
    #Function for handling initialize button press
    def initializeButton(self):
        
        #Set up a progress bar
        self.progress=ttk.Progressbar(self,orient='horizontal',length=300,mode='determinate')
        self.init_button_window = self.canvas.create_window(900/2,0.35*507,anchor='center',window=self.progress)

        #Destroy the initialize button since it gets replaced by the progress bar
        self.init_button.destroy()

        #Define a as our global variable to communicate with the spectrometer
        global a
        a=Spectrometer(usb)

        #Set up spectrometer and update the progress bar through each step
        a.on()

	#wait message (NOTE: background covers this so this is commented out until solution is found)
        #self.waitMessage = tk.Label(self,text = "Please wait, this may take a while...")
        #self.plottingMenuFont = ("jua",12)
        #self.waitMessage.config(font=self.plottingMenuFont)
        #self.waitMessage.place(relx=0.5,rely=0.5,anchor=tk.CENTER)	
	
        self.progress['value']=25
        self.progress.update()
        a.initialize()
        self.progress['value']=50
        self.progress.update()
        a.setMotorSpeed()
        self.progress['value']=60
        self.progress.update()
        a.setSlitSpeed('0')
        self.progress['value']=70
        self.progress.update()
        a.setSlitSpeed('1')
        self.progress['value']=80
        self.progress.update()
        a.setSlitSpeed('2')
        self.progress['value']=90
        self.progress.update()
        a.setSlitSpeed('3')
        self.progress['value']=100
        self.progress.update()

        #When finished, go to the main menu
        self.controller.show_frame(MainMenu)

#Our main menu class
class MainMenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller

        #Main Menu Text Label
        self.label = tk.Label(self,text = "Main Menu")
        self.MainMenuFont = ("jua",40,"bold")
        self.label.config(font=self.MainMenuFont)
        self.label.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
        
        #Create a label for each button (Information, Scanning, Tool Control) and place them evenly spaced apart 
        self.button1Frame = ttk.Label(self)
        self.button1Frame.place(relx=0.24,rely=0.27,anchor=tk.CENTER)

        self.button1 = tk.Button(self.button1Frame, text="Information",command=self.infoButton)
        self.buttonFont = ("jua",15,'bold')
        self.button1.config(font=self.buttonFont)
        self.button1.grid(column=0,row=1)
        self.button1.config(height=2,width=25)

        self.button2Frame = ttk.Label(self)
        self.button2Frame.place(relx=0.24,rely=0.54,anchor=tk.CENTER)

        self.button2 = tk.Button(self.button2Frame, text="Scanning",command=self.scanButton)
        self.buttonFont = ("jua",15,'bold')
        self.button2.config(font=self.buttonFont)
        self.button2.grid(column=0,row=3)
        self.button2.config(height=2,width=25)

        self.button3Frame = ttk.Label(self)
        self.button3Frame.place(relx=0.24,rely=0.81,anchor=tk.CENTER)

        self.button3 = tk.Button(self.button3Frame, text="Tool Control",command=self.toolButton)
        self.buttonFont = ("jua",15,'bold')
        self.button3.config(font=self.buttonFont)
        self.button3.grid(column=0,row=3)
        self.button3.config(height=2,width=25)

        #Place images to the right of the buttons for design purposes
        self.image1 = Image.open("Main1.png")
        self.image1 = self.image1.resize((250,200),Image.ANTIALIAS)
        self.imageHold1 = tk.Canvas(self)
        self.image1 = ImageTk.PhotoImage(self.image1)
        self.imageHold1.create_image(0,0,image=self.image1,anchor='nw')
        self.imageHold1.place(relx=0.7,rely=0.47,anchor=tk.CENTER)

        self.image2 = Image.open("Main2.png")
        self.image2 = self.image2.resize((250,200),Image.ANTIALIAS)
        self.imageHold2 = tk.Canvas(self)
        self.image2 = ImageTk.PhotoImage(self.image2)
        self.imageHold2.create_image(0,0,image=self.image2,anchor='nw')
        self.imageHold2.place(relx=0.88,rely=0.77,anchor=tk.CENTER)

    #Functions for handling button presses from main menu
    def infoButton(self):
        self.controller.show_frame(Information)

    def scanButton(self):
        #Make the window bigger for the scanning menu so the user can see the plot well enough
        window.geometry('1500x900')

        self.controller.show_frame(Scanning)

    def toolButton(self):
        self.controller.show_frame(Tools)

#Our information page (Not finished as of week of 12/2)
class Information(tk.Frame):

    def __init__(self,parent,controller):
        self.controller = controller
        imageName = 'Slide1.jpeg'
        w = 900
        h = 507
        tk.Frame.__init__(self,parent)

#Our scanning page
class Scanning(tk.Frame):

    def __init__(self,parent,controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)

        #If you want the window to be resizeable:
        #window.resizable(width=True,height=True)

        #Scanning Menu Title Label
        self.label = tk.Label(self,text = "Scanning")
        self.ScanningMenuFont = ("jua",35,"bold")
        self.label.config(font=self.ScanningMenuFont)
        self.label.place(relx=0.5,rely=0.07,anchor=tk.CENTER)

        #Variables to store step values and intensities
        self.steps = []
        self.intensities = []

        #Read in the sample data for the sample plot and store values
        with open('thorlabsBulb.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.steps.append(row['wavelength'])
                self.intensities.append(row['intensity'])
        
        #Variables to store plot options
        self.color = 'b'
        self.plotTitle = 'Sample Spectrum'
        self.xlabel = 'Wavelength (nm)'
        self.ylabel = 'Intensity'

        #Plot the sample spectrum     
        self.f = Figure(figsize=(7,5.4),dpi=100)
        self.sample = self.f.add_subplot(111)
        self.sample.plot(self.steps,self.intensities,self.color)
        self.sample.set_title(self.plotTitle)
        self.sample.set_xlabel(self.xlabel)
        self.sample.set_ylabel(self.ylabel)
        self.xmin, self.xmax = self.sample.get_xlim()
        self.ymin, self.ymax = self.sample.get_ylim()

        #Create canvas for the plot and add it to the window
        self.pltcanvas = FigureCanvasTkAgg(self.f,self)
        self.pltcanvas.show()
        self.pltcanvas.get_tk_widget().place(relx=0.72,rely=0.5,anchor=tk.CENTER)

        #Button for returning to main menu
        self.button1Frame = ttk.Label(self)
        self.button1Frame.place(relx=0.062,rely=0.07,anchor=tk.CENTER)
        self.button1 = tk.Button(self.button1Frame, text="Main Menu",command=self.menuButton)
        self.buttonFont = ("jua",10,'bold')
        self.button1.config(font=self.buttonFont)
        self.button1.grid(column=0,row=1)
        self.button1.config(height=2,width=10)

        #Button for downloading png image
        self.pngFrame = ttk.Label(self)
        self.pngFrame.place(relx=0.568,rely=0.86,anchor=tk.CENTER)
        self.png = tk.Button(self.pngFrame, text="Export PNG",command=self.pngButton)
        self.buttonFont = ("jua",10,'bold')
        self.png.config(font=self.buttonFont)
        self.png.grid(column=0,row=1)
        self.png.config(height=2,width=11)

        #Button for downloading jpg image
        self.jpgFrame = ttk.Label(self)
        self.jpgFrame.place(relx=0.668,rely=0.86,anchor=tk.CENTER)
        self.jpg = tk.Button(self.jpgFrame, text="Export JPG",command=self.jpgButton)
        self.buttonFont = ("jua",10,'bold')
        self.jpg.config(font=self.buttonFont)
        self.jpg.grid(column=0,row=1)
        self.jpg.config(height=2,width=11)

        #Button for downloading csv file
        self.csvFrame = ttk.Label(self)
        self.csvFrame.place(relx=0.768,rely=0.86,anchor=tk.CENTER)
        self.csv = tk.Button(self.csvFrame, text="Export CSV",command=self.csvButton)
        self.buttonFont = ("jua",10,'bold')
        self.csv.config(font=self.buttonFont)
        self.csv.grid(column=0,row=1)
        self.csv.config(height=2,width=11)

        #Button for opening plot options
        self.pltOptionFrame = ttk.Label(self)
        self.pltOptionFrame.place(relx=0.868,rely=0.86,anchor=tk.CENTER)
        self.pltOption = tk.Button(self.pltOptionFrame, text="Plot Options",command=self.plotMenuButton)
        self.buttonFont = ("jua",10,'bold')
        self.pltOption.config(font=self.buttonFont)
        self.pltOption.grid(column=0,row=1)
        self.pltOption.config(height=2,width=11)

        #Button for opening help window
        self.helpFrame = ttk.Label(self)
        self.helpFrame.place(relx=0.44,rely=0.22,anchor=tk.CENTER)
        self.helpOption = tk.Button(self.helpFrame, text="Help",command=self.helpButton)
        self.buttonFont = ("jua",10,'bold')
        self.helpOption.config(font=self.buttonFont)
        self.helpOption.grid(column=0,row=1)
        self.helpOption.config(height=2,width=11)

        #Title label for range options
        self.rangeLabel = tk.Label(self,text = "Range:")
        self.ScanningMenuFont = ("jua",20,"bold")
        self.rangeLabel.config(font=self.ScanningMenuFont)
        self.rangeLabel.place(relx=0.06,rely=0.17,anchor=tk.CENTER)

        #Small label for low input and entry box
        self.lowLabel = tk.Label(self,text = "Low:")
        self.ScanningMenuFont = ("jua",12)
        self.lowLabel.config(font=self.ScanningMenuFont)
        self.lowLabel.place(relx=0.038,rely=0.22,anchor=tk.CENTER)
        self.lowEntry=tk.Entry(self)
        self.lowEntry.place(relx=0.11,rely=0.22,anchor=tk.CENTER)

        #nm label
        self.nmLabel = tk.Label(self,text = "nm")
        self.ScanningMenuFont = ("jua",9)
        self.nmLabel.config(font=self.ScanningMenuFont)
        self.nmLabel.place(relx=0.175,rely=0.22,anchor=tk.CENTER)

        #Small label for high input and entry box
        self.highLabel = tk.Label(self,text = "High:")
        self.ScanningMenuFont = ("jua",12)
        self.highLabel.config(font=self.ScanningMenuFont)
        self.highLabel.place(relx=0.238,rely=0.22,anchor=tk.CENTER)
        self.highEntry=tk.Entry(self)
        self.highEntry.place(relx=0.31,rely=0.22,anchor=tk.CENTER)

        #nm label
        self.nmLabel2 = tk.Label(self,text = "nm")
        self.ScanningMenuFont = ("jua",9)
        self.nmLabel2.config(font=self.ScanningMenuFont)
        self.nmLabel2.place(relx=0.375,rely=0.22,anchor=tk.CENTER)

        #Title label for entrance slit option
        self.slitEntLabel = tk.Label(self,text = "Entrance Slit Width:")
        self.ScanningMenuFont = ("jua",20,"bold")
        self.slitEntLabel.config(font=self.ScanningMenuFont)
        self.slitEntLabel.place(relx=0.125,rely=0.27,anchor=tk.CENTER)

        #Entrance slit width slider
        self.entSlider = tk.Scale(self, from_=0, to=10000, orient=HORIZONTAL, length=580,resolution=12.5,digits=5)
        self.entSlider.place(relx=0.218,rely=0.32,anchor=tk.CENTER)

        #Micrometer label
        self.mLabel = tk.Label(self,text = "\u03BCm")
        self.ScanningMenuFont = ("jua",9)
        self.mLabel.config(font=self.ScanningMenuFont)
        self.mLabel.place(relx=0.420,rely=0.33,anchor=tk.CENTER)

        #Title label for exit slit option
        self.slitExtLabel = tk.Label(self,text = "Exit Slit Width:")
        self.ScanningMenuFont = ("jua",20,"bold")
        self.slitExtLabel.config(font=self.ScanningMenuFont)
        self.slitExtLabel.place(relx=0.1,rely=0.38,anchor=tk.CENTER)

        #Exit slit width slider
        self.extSlider = tk.Scale(self, from_=0, to=10000, orient=HORIZONTAL, length=580,resolution=12.5,digits=5)
        self.extSlider.place(relx=0.218,rely=0.43,anchor=tk.CENTER)

        #Micrometer label
        self.mLabel2 = tk.Label(self,text = "\u03BCm")
        self.ScanningMenuFont = ("jua",9)
        self.mLabel2.config(font=self.ScanningMenuFont)
        self.mLabel2.place(relx=0.420,rely=0.44,anchor=tk.CENTER)

        #Title label for integration time option
        self.intTimeLabel = tk.Label(self,text = "Integration Time:")
        self.ScanningMenuFont = ("jua",20,"bold")
        self.intTimeLabel.config(font=self.ScanningMenuFont)
        self.intTimeLabel.place(relx=0.113,rely=0.49,anchor=tk.CENTER)

        #Integration time slider
        self.intSlider = tk.Scale(self, from_=1, to=200, orient=HORIZONTAL, length=580,resolution=1)
        self.intSlider.place(relx=0.218,rely=0.54,anchor=tk.CENTER)

        #Seconds label
        self.sLabel = tk.Label(self,text = "ms")
        self.ScanningMenuFont = ("jua",9)
        self.sLabel.config(font=self.ScanningMenuFont)
        self.sLabel.place(relx=0.420,rely=0.55,anchor=tk.CENTER)

        #Title label for step size option
        self.stepLabel = tk.Label(self,text = "Step Size:")
        self.ScanningMenuFont = ("jua",20,"bold")
        self.stepLabel.config(font=self.ScanningMenuFont)
        self.stepLabel.place(relx=0.075,rely=0.60,anchor=tk.CENTER)

        #Step size slider
        self.stepSlider = tk.Scale(self, from_=0.0041666667, to=5, orient=HORIZONTAL, length=580,resolution=0.0041666667,digits=11)
        self.stepSlider.place(relx=0.218,rely=0.65,anchor=tk.CENTER)

        #Nanometers label
        self.nmLabel3 = tk.Label(self,text = "nm")
        self.ScanningMenuFont = ("jua",9)
        self.nmLabel3.config(font=self.ScanningMenuFont)
        self.nmLabel3.place(relx=0.420,rely=0.66,anchor=tk.CENTER)

        #Title label for grating option
        self.gratingLabel = tk.Label(self,text = "Grating:")
        self.ScanningMenuFont = ("jua",20,"bold")
        self.gratingLabel.config(font=self.ScanningMenuFont)
        self.gratingLabel.place(relx=0.065,rely=0.71,anchor=tk.CENTER)

        #Drop-down menu for grating options (Note: gratingDefault is the actual menu, I originally thought this was just a way to set the default)
        self.gratingDefault = StringVar(self)
        self.gratingDefault.set('1800 l/mm (Vis)') #This sets the default
        self.gratingBox = OptionMenu(self,self.gratingDefault,'1800 l/mm (Vis)','600 l/mm (IR)', command = self.stepChange)
        self.gratingBox.place(relx=0.065,rely=0.76,anchor=tk.CENTER)

        #Title label for detector option
        self.detectorLabel = tk.Label(self,text = "Detector:")
        self.ScanningMenuFont = ("jua",20,"bold")
        self.detectorLabel.config(font=self.ScanningMenuFont)
        self.detectorLabel.place(relx=0.23,rely=0.71,anchor=tk.CENTER)

        #Drop-down menu for detector options (Note: detectorDefault is the actual menu, I originally thought this was just a way to set the default)
        self.detectorDefault = StringVar(self)
        self.detectorDefault.set('Side')
        self.detectorBox = OptionMenu(self,self.detectorDefault,'Side','Front')
        self.detectorBox.place(relx=0.23,rely=0.76,anchor=tk.CENTER)

        #Title label for the gain option
        self.gainLabel = tk.Label(self,text = "Gain:")
        self.ScanningMenuFont = ("jua",20,"bold")
        self.gainLabel.config(font=self.ScanningMenuFont)
        self.gainLabel.place(relx=0.39,rely=0.71,anchor=tk.CENTER)

        #Drop-down menu for gain options (Note: gainDefault is the actual menu, I originally thought this was just a way to set the default)
        self.gainDefault = StringVar(self)
        self.gainDefault.set('AUTO')
        self.gainBox = OptionMenu(self,self.gainDefault,'AUTO','1x','10x','100x','1000x')
        self.gainBox.place(relx=0.39,rely=0.76,anchor=tk.CENTER)

        #Button to start scan and collect all input
        self.startButtonFrame = ttk.Label(self)
        self.startButtonFrame.place(relx=0.22,rely=0.85,anchor=tk.CENTER)
        self.startButton = tk.Button(self.startButtonFrame, text="Start Scan",command=self.startScanButton)
        self.buttonFont = ("jua",14,'bold')
        self.startButton.config(font=self.buttonFont)
        self.startButton.grid(column=0,row=1)
        self.startButton.config(height=2,width=15)

        #Error Label Definitions:

        #Low value is nan
        self.errorLabelLow = tk.Label(self,text = "Error: Low range value entered is not a number! Please enter again!")
        self.errorFont = ("jua",12,"bold")
        self.errorLabelLow.config(font=self.errorFont,foreground='red')

        #High value is nan
        self.errorLabelHigh = tk.Label(self,text = "Error: High range value entered is not a number! Please enter again!")
        self.errorLabelHigh.config(font=self.errorFont,foreground='red')

        #Low greater than high
        self.highLow = tk.Label(self,text = "Error: Low range value exceeds or equals high range value!")
        self.highLow.config(font=self.errorFont,foreground='red')

        #Range out of bounds (visible)
        self.outOfRange1800 = tk.Label(self,text = "Error: Range must be between 300nm and 869.5875069567nm for 1800 grating!")
        self.outOfRange1800.config(font=self.errorFont,foreground='red')

        #Range out of bounds (IR)
        self.outOfRange600 = tk.Label(self,text = "Error: Range must be between 300nm and 1000nm for 600 grating!")
        self.outOfRange600.config(font=self.errorFont,foreground='red')

        #Can't have just 1 data point or 0 data points
        self.stepRange = tk.Label(self,text = "Error: Step size exceeds or equals scanning range!")
        self.stepRange.config(font=self.errorFont,foreground='red')

        #Spectrometer has 5000 data point capacity limit
        self.dataRange = tk.Label(self,text = "Error: Number of data points exceeds 5000 with selected step size!")
        self.dataRange.config(font=self.errorFont,foreground='red')

        #Something went wrong in set scan function
        self.setScanError = tk.Label(self,text = "Error: Scanning malfunction (Setting Scan)! Please restart device and application!")
        self.setScanError.config(font=self.errorFont,foreground='red')

        #Something went wrong in start scan function
        self.setScanError2 = tk.Label(self,text = "Error: Scanning malfunction (Starting Scan)! Please restart device and application!")
        self.setScanError2.config(font=self.errorFont,foreground='red')

        #Successfully started scan
        self.progressStart = tk.Label(self,text = "Starting scan...")
        self.progressStart.config(font=self.errorFont,foreground='red')

        #Setup of parameters
        self.progressSetting = tk.Label(self,text = "Setting scan parameters...")
        self.progressSetting.config(font=self.errorFont,foreground='red')

        #Spectrometer scanning
        self.progressScanning = tk.Label(self,text = "Scanning...")
        self.progressScanning.config(font=self.errorFont,foreground='red')

        #Scan completed! Getting data
        self.progressData = tk.Label(self,text = "Downloading data...")
        self.progressData.config(font=self.errorFont,foreground='red')

        #Re-initializes after each scan
        self.progressInit = tk.Label(self,text = "Re-initializing...")
        self.progressInit.config(font=self.errorFont,foreground='red')

        #Initializing the labels for the download success text (Don't know why I didn't add the text yet)
        self.csvDownload = tk.Label(self)
        self.csvDownload.config(font=self.errorFont,foreground='red')

        self.pngDownload = tk.Label(self)
        self.pngDownload.config(font=self.errorFont,foreground='red')

        self.jpgDownload = tk.Label(self)
        self.jpgDownload.config(font=self.errorFont,foreground='red')

        #Initialize the progress bar for when scanning
        self.progress=ttk.Progressbar(self,orient='horizontal',length=300,mode='indeterminate')
    #stepChange function
    def stepChange(self, grating):
        self.stepSlider.destroy()
        if grating == '1800 l/mm (Vis)':
           self.stepSlider = tk.Scale(self, from_=0.0041666667, to=5, orient=HORIZONTAL, length=580,resolution=0.0041666667,digits=11)
           self.stepSlider.place(relx=0.218,rely=0.65,anchor=tk.CENTER)
        elif grating == '600 l/mm (IR)':
           self.stepSlider = tk.Scale(self, from_=0.0125, to=5, orient=HORIZONTAL, length=580,resolution=0.0125,digits=11)
           self.stepSlider.place(relx=0.218,rely=0.65,anchor=tk.CENTER)
           
    #Function to handle main menu button push
    def menuButton(self):
        window.geometry('900x507')
        self.controller.show_frame(MainMenu)

    #Function for handling plot options button push
    def plotMenuButton(self):

        #Lock all scan features
        self.startButton.configure(state=DISABLED)
        self.gainBox.config(state=DISABLED)
        self.detectorBox.config(state=DISABLED)
        self.gratingBox.config(state=DISABLED)
        self.stepSlider.config(state=DISABLED)
        self.intSlider.config(state=DISABLED)
        self.extSlider.config(state=DISABLED)
        self.entSlider.config(state=DISABLED)
        self.highEntry.config(state=DISABLED)
        self.lowEntry.config(state=DISABLED)
        self.csv.config(state=DISABLED)
        self.jpg.config(state=DISABLED)
        self.png.config(state=DISABLED)
        self.pltOption.config(state=DISABLED)

        #Make sure the graphics get caught up
        self.update()

        #Create window for options
        self.win = tk.Toplevel()
        self.win.wm_title("Plot Options")
        self.win.resizable(width=False,height=False)
        
        #Calculations for the values needed to put new window in the center of the screen
        width = 460
        height = 460
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws/2) - (width/2))
        y = int((hs/2) - (height/2))
        width = str(width)
        height = str(height)
        x = str(x)
        y = str(y)

        #Position window
        self.win.geometry(width + 'x' + height + '+' + x + '+' + y)

        #Title label for plot options menu
        menuTitle = tk.Label(self.win, text="Plot Options Menu")
        menuTitle.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
        self.plottingTitleFont = ("jua",16,"bold")
        menuTitle.config(font=self.plottingTitleFont)

        #Button for applying changes and collecting user input
        applyButtonFrame = tk.Label(self.win)
        applyButtonFrame.place(relx=0.5,rely=0.91,anchor=tk.CENTER)
        applyButton = tk.Button(applyButtonFrame, text="Apply Changes",command=self.applyChanges)
        buttonFont = ("jua",12,'bold')
        applyButton.config(font=buttonFont, height=1, width=12)
        applyButton.grid(column=0,row=1)

        #Option for changing plot title (Text Entry)
        self.titleLabel = tk.Label(self.win,text = "Plot Title:")
        self.plottingMenuFont = ("jua",12)
        self.titleLabel.config(font=self.plottingMenuFont)
        self.titleLabel.place(relx=0.2,rely=0.22,anchor=tk.CENTER)
        self.titleEntry=tk.Entry(self.win)
        self.titleEntry.config(width=30)
        self.titleEntry.place(relx=0.66,rely=0.22,anchor=tk.CENTER)

        #Option for changing plot type (Drop down)
        self.typeLabel = tk.Label(self.win,text = "Plot Type:")
        self.plottingMenuFont = ("jua",12)
        self.typeLabel.config(font=self.plottingMenuFont)
        self.typeLabel.place(relx=0.2,rely=0.32,anchor=tk.CENTER)
        self.typeDefault = StringVar(self.win)
        self.typeDefault.set('Line Plot')
        self.typeBox = OptionMenu(self.win,self.typeDefault,'Line Plot','Scatter Plot')
        self.typeBox.place(relx=0.495,rely=0.32,anchor=tk.CENTER)

        #Option for changing minimum wavelength on plot (Entry)
        self.xminLabel = tk.Label(self.win,text = "Min Wavelength:")
        self.plottingMenuFont = ("jua",12)
        self.xminLabel.config(font=self.plottingMenuFont)
        self.xminLabel.place(relx=0.2,rely=0.42,anchor=tk.CENTER)
        self.xminEntry=tk.Entry(self.win)
        self.xminEntry.config(width=15)
        self.xminEntry.place(relx=0.532,rely=0.42,anchor=tk.CENTER)

        #Option for changing maximum wavelength on plot (Entry)
        self.xmaxLabel = tk.Label(self.win,text = "Max Wavelength:")
        self.plottingMenuFont = ("jua",12)
        self.xmaxLabel.config(font=self.plottingMenuFont)
        self.xmaxLabel.place(relx=0.2,rely=0.52,anchor=tk.CENTER)
        self.xmaxEntry=tk.Entry(self.win)
        self.xmaxEntry.config(width=15)
        self.xmaxEntry.place(relx=0.532,rely=0.52,anchor=tk.CENTER)

        #Option for changing minimum intensity on plot (Entry)
        self.yminLabel = tk.Label(self.win,text = "Min Intensity:")
        self.plottingMenuFont = ("jua",12)
        self.yminLabel.config(font=self.plottingMenuFont)
        self.yminLabel.place(relx=0.2,rely=0.62,anchor=tk.CENTER)
        self.yminEntry=tk.Entry(self.win)
        self.yminEntry.config(width=15)
        self.yminEntry.place(relx=0.532,rely=0.62,anchor=tk.CENTER)

        #Option for changing maximum intensity on plot (Entry)
        self.ymaxLabel = tk.Label(self.win,text = "Max Intensity:")
        self.plottingMenuFont = ("jua",12)
        self.ymaxLabel.config(font=self.plottingMenuFont)
        self.ymaxLabel.place(relx=0.2,rely=0.72,anchor=tk.CENTER)
        self.ymaxEntry=tk.Entry(self.win)
        self.ymaxEntry.config(width=15)
        self.ymaxEntry.place(relx=0.532,rely=0.72,anchor=tk.CENTER)

        #Option for changing color of plot (Drop-down)
        self.colorLabel = tk.Label(self.win,text = "Plot Color:")
        self.plottingMenuFont = ("jua",12)
        self.colorLabel.config(font=self.plottingMenuFont)
        self.colorLabel.place(relx=0.2,rely=0.82,anchor=tk.CENTER)
        self.colorDefault = StringVar(self.win)
        self.colorDefault.set('Blue')
        self.colorBox = OptionMenu(self.win,self.colorDefault,'Blue','Red','Green','Black','Cyan')
        self.colorBox.place(relx=0.47,rely=0.82,anchor=tk.CENTER)
        
        #Used for if the user closes the window with the red x instead of pressing the apply button
        self.win.protocol("WM_DELETE_WINDOW",self.callback)


    def helpButton(self):
        #Lock all scan features
        self.startButton.configure(state=DISABLED)
        self.gainBox.config(state=DISABLED)
        self.detectorBox.config(state=DISABLED)
        self.gratingBox.config(state=DISABLED)
        self.stepSlider.config(state=DISABLED)
        self.intSlider.config(state=DISABLED)
        self.extSlider.config(state=DISABLED)
        self.entSlider.config(state=DISABLED)
        self.highEntry.config(state=DISABLED)
        self.lowEntry.config(state=DISABLED)
        self.csv.config(state=DISABLED)
        self.jpg.config(state=DISABLED)
        self.png.config(state=DISABLED)
        self.pltOption.config(state=DISABLED)
        self.update()

        self.win = tk.Toplevel()
        self.win.wm_title("Help Bar")
        self.win.resizable(width=False,height=False)
        
        #Values for positioning of window in center
        width = 620
        height = 150
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws/2) - (width/2))
        y = int((hs/2) - (height/2))
        width = str(width)
        height = str(height)
        x = str(x)
        y = str(y)

        #Position window
        self.win.geometry(width + 'x' + height + '+' + x + '+' + y)

        #Buttons and options
        menuTitle = tk.Label(self.win, text="Help")
        menuTitle.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
        self.plottingTitleFont = ("jua",16,"bold")
        menuTitle.config(font=self.plottingTitleFont)
	
	#inform user of possible wavelength ranges for given grating
        grating = self.gratingDefault.get()
        self.titleLabel = tk.Label(self.win,text = "Valid Wavelength Ranges for {}:".format(grating))
        self.titleLabelFont = ("jua",12)
        self.titleLabel.config(font=self.titleLabelFont)
        self.titleLabel.place(relx=0.44,rely=0.30,anchor=tk.CENTER)
        
        #Place ranges for specified grating
        if grating == '1800 l/mm (Vis)':
            self.rangeLabel = tk.Label(self.win,text = 'Choose range between 300nm and 869.5875069567nm')
            self.rangeLabel.place(relx=0.51,rely=0.45,anchor=tk.CENTER)
        elif grating == '600 l/mm (IR)':
            self.rangeLabel = tk.Label(self.win,text = 'Choose range between 300nm and 1000nm')
            self.rangeLabel.place(relx=0.44,rely=0.45,anchor=tk.CENTER)
        self.rangeLabelFont = ("jua",12)
        self.rangeLabel.config(font=self.rangeLabelFont)
	
        #Note that at 300nm actually observing 300.0000024nm due to stepsize limitations
        self.noteLabel = tk.Label(self.win,text = 'Note at 300nm you actually are observing 300.0000024nm due to smallest step size limitation.')
        self.noteLabel.place(relx=0.50,rely=0.80,anchor=tk.CENTER)
        self.noteLabelFont = ("jua",8)
        self.noteLabel.config(font=self.noteLabelFont)
        
        self.win.protocol("WM_DELETE_WINDOW",self.callback)

    #Function to handle plot options window being closed with red x built in to system
    def callback(self):
        #Re-enable all scan features
        self.startButton.configure(state=NORMAL)
        self.gainBox.config(state=NORMAL)
        self.detectorBox.config(state=NORMAL)
        self.gratingBox.config(state=NORMAL)
        self.stepSlider.config(state=NORMAL)
        self.intSlider.config(state=NORMAL)
        self.extSlider.config(state=NORMAL)
        self.entSlider.config(state=NORMAL)
        self.highEntry.config(state=NORMAL)
        self.lowEntry.config(state=NORMAL)
        self.csv.config(state=NORMAL)
        self.jpg.config(state=NORMAL)
        self.png.config(state=NORMAL)
        self.pltOption.config(state=NORMAL)

        #Catch graphics up
        self.update()

        #Get rid of the pop-up window
        self.win.destroy()

    #Function to handle file select window being closed with red x built in to system
    def callbackExport(self):

        #Turn on buttons again
        self.csv.config(state=NORMAL)
        self.jpg.config(state=NORMAL)
        self.png.config(state=NORMAL)
        self.pltOption.config(state=NORMAL)

    #Function to handle apply button push in plot options menu
    def applyChanges(self):

        #Collect all the input
        title = self.titleEntry.get()
        ptype = self.typeDefault.get()
        xmin = self.xminEntry.get()
        ymin = self.yminEntry.get()
        xmax = self.xmaxEntry.get()
        ymax = self.ymaxEntry.get()
        color = self.colorDefault.get()

        #If the user doesn't input a title, use the default
        if title=='':
           title=self.plotTitle
        else:
           self.plotTitle = title

        #Store the selected color
        if color == 'Blue':
           self.color='b'
        if color == 'Black':
           self.color='k'
        if color == 'Red':
           self.color='r'
        if color == 'Green':
           self.color='g'
        if color == 'Cyan':
           self.color='c'

        #If the user didn't input an actual number, use the default
        if self.is_number(xmin)==False:
           xmin = self.xmin
        else:
           xmin = float(xmin)
        if self.is_number(xmax)==False:
           xmax = self.xmax
        else:
           xmax = float(xmax)
        if self.is_number(ymin)==False:
           ymin = self.ymin
        else:
           ymin = float(ymin)
        if self.is_number(ymax)==False:
           ymax = self.ymax
        else:
           ymax = float(ymax)

        #If the user wanted a scatter plot, make one and update
        if ptype=="Scatter":
           
           #Create and display plot:
           self.f = Figure(figsize=(7,5.4),dpi=100)
           self.sample = self.f.add_subplot(111)
           self.sample.scatter(self.steps,self.intensities,self.color)
           self.sample.set_title(self.plotTitle)
           self.sample.set_xlabel(self.xlabel)
           self.sample.set_ylabel(self.ylabel)
           self.sample.set_xlim(xmin,xmax)
           self.sample.set_ylim(ymin,ymax)

           self.pltcanvas = FigureCanvasTkAgg(self.f,self)
           self.pltcanvas.show()
           self.pltcanvas.get_tk_widget().place(relx=0.72,rely=0.5,anchor=tk.CENTER)
           self.update()

        #If the user wanted a line plot, make one and update
        else:
           #Create and display plot:
           self.f = Figure(figsize=(7,5.4),dpi=100)
           self.sample = self.f.add_subplot(111)
           self.sample.plot(self.steps,self.intensities,self.color)
           self.sample.set_title(self.plotTitle)
           self.sample.set_xlabel(self.xlabel)
           self.sample.set_ylabel(self.ylabel)
           self.sample.set_xlim(xmin,xmax)
           self.sample.set_ylim(ymin,ymax)

           self.pltcanvas = FigureCanvasTkAgg(self.f,self)
           self.pltcanvas.show()
           self.pltcanvas.get_tk_widget().place(relx=0.72,rely=0.5,anchor=tk.CENTER)
           self.update()
           
        #Clear the plot options window
        self.win.destroy()
        
        #Re-enable all scan features
        self.startButton.configure(state=NORMAL)
        self.gainBox.config(state=NORMAL)
        self.detectorBox.config(state=NORMAL)
        self.gratingBox.config(state=NORMAL)
        self.stepSlider.config(state=NORMAL)
        self.intSlider.config(state=NORMAL)
        self.extSlider.config(state=NORMAL)
        self.entSlider.config(state=NORMAL)
        self.highEntry.config(state=NORMAL)
        self.lowEntry.config(state=NORMAL)
        self.csv.config(state=NORMAL)
        self.jpg.config(state=NORMAL)
        self.png.config(state=NORMAL)
        self.pltOption.config(state=NORMAL)

        #Make sure graphics catch up
        self.update()

    #Function to handle png download button push
    def pngButton(self):

        #Don't allow user to double click or select others
        self.csv.config(state=DISABLED)
        self.jpg.config(state=DISABLED)
        self.png.config(state=DISABLED)
        self.pltOption.config(state=DISABLED)

        #Forget old message
        self.csvDownload.place_forget()
        self.pngDownload.place_forget()
        self.jpgDownload.place_forget()

        #Make sure graphics catch up
        self.update()

        #Give user the option for file location
        f = filedialog.asksaveasfile(mode='w',defaultextension='.png')

        #As long as there was a file name entered...
        if not f is None:
           self.f.savefig(f.name)

           f.close()

           #Display message that download successful
           self.pngDownload = tk.Label(self, text='Downloaded PNG as ' + f.name)
           self.pngDownload.config(font=self.errorFont)
           self.pngDownload.place(relx=0.721,rely=0.94,anchor=tk.CENTER)

        #Turn on buttons again
        self.csv.config(state=NORMAL)
        self.jpg.config(state=NORMAL)
        self.png.config(state=NORMAL)
        self.pltOption.config(state=NORMAL)

    #Function to handle jpg download button push
    def jpgButton(self):

        #Don't allow user to double click
        self.csv.config(state=DISABLED)
        self.jpg.config(state=DISABLED)
        self.png.config(state=DISABLED)
        self.pltOption.config(state=DISABLED)

        #Forget old message
        self.csvDownload.place_forget()
        self.pngDownload.place_forget()
        self.jpgDownload.place_forget()
        self.update()

        #Give user the option for file location
        f = filedialog.asksaveasfile(mode='w',defaultextension='.jpg')

        #As long as there was a file name entered...
        if not f is None:
           self.f.savefig(f.name)

           f.close()

           #Display message that download successful
           self.jpgDownload = tk.Label(self, text='Downloaded JPG as ' + f.name)
           self.jpgDownload.config(font=self.errorFont)
           self.jpgDownload.place(relx=0.721,rely=0.94,anchor=tk.CENTER)

        #Turn on buttons again
        self.csv.config(state=NORMAL)
        self.jpg.config(state=NORMAL)
        self.png.config(state=NORMAL)
        self.pltOption.config(state=NORMAL)

    #Function to handle csv download button push
    def csvButton(self):

        #Don't allow user to double click
        self.csv.config(state=DISABLED)
        self.jpg.config(state=DISABLED)
        self.png.config(state=DISABLED)
        self.pltOption.config(state=DISABLED)

        #Forget old message
        self.csvDownload.place_forget()
        self.pngDownload.place_forget()
        self.jpgDownload.place_forget()
        self.update()

        #Give user the option for file location
        f = filedialog.asksaveasfile(mode='w',defaultextension='.csv')

        #As long as file name entered...
        if not f is None:
           f.write('Wavelength(nm),Intensities\n')
           for i in range(len(self.steps)):
               f.write(str(self.steps[i]))
               f.write(',')
               f.write(str(self.intensities[i]))
               f.write('\n')

           f.close()

           #Display message that download successful
           self.csvDownload = tk.Label(self, text='Downloaded CSV as ' + f.name)
           self.csvDownload.config(font=self.errorFont)
           self.csvDownload.place(relx=0.721,rely=0.94,anchor=tk.CENTER)

        #Turn on buttons again
        self.csv.config(state=NORMAL)
        self.jpg.config(state=NORMAL)
        self.png.config(state=NORMAL)
        self.pltOption.config(state=NORMAL)
        
    #Function used to check if input from user is a number (Used in scanning menu, plot options menu, and tool control menu)
    def is_number(self,a):
        try:
            float(a)
            return True
        except ValueError:
            pass

        return False

    #Function used to clear all possible errors
    def clearErrors(self):

        #Clear all errors before proceeding
        self.errorLabelLow.place_forget()
        self.errorLabelHigh.place_forget()
        self.outOfRange1800.place_forget()
        self.outOfRange600.place_forget()
        self.highLow.place_forget()
        self.stepRange.place_forget()
        self.dataRange.place_forget()
        self.setScanError.place_forget()
        self.setScanError2.place_forget()
        self.progressStart.place_forget()
        self.progressSetting.place_forget()
        self.progressScanning.place_forget()
        self.progressData.place_forget()
        self.progressInit.place_forget()
        self.csvDownload.place_forget()
        self.pngDownload.place_forget()
        self.jpgDownload.place_forget()

    #Function used to handle start scan button push (LONG!!!)
    def startScanButton(self):

        #Make sure all errors cleared and graphics caught up
        self.clearErrors()
        self.update()

        #Don't allow user to enter anything more
        self.startButton.configure(state=DISABLED)
        self.gainBox.config(state=DISABLED)
        self.detectorBox.config(state=DISABLED)
        self.gratingBox.config(state=DISABLED)
        self.stepSlider.config(state=DISABLED)
        self.intSlider.config(state=DISABLED)
        self.extSlider.config(state=DISABLED)
        self.entSlider.config(state=DISABLED)
        self.highEntry.config(state=DISABLED)
        self.lowEntry.config(state=DISABLED)
        self.csv.config(state=DISABLED)
        self.jpg.config(state=DISABLED)
        self.png.config(state=DISABLED)
        self.pltOption.config(state=DISABLED)

        #Collect all the user input
        low = self.lowEntry.get()
        high = self.highEntry.get()
        gain = self.gainDefault.get()
        grating = self.gratingDefault.get()
        detector = self.detectorDefault.get()
        entSize = self.entSlider.get()
        extSize = self.extSlider.get()
        stepSize = self.stepSlider.get()
        intTime = self.intSlider.get()


        #Check if low value is a number:
        if self.is_number(low)==False:

            #If it isn't throw an error at user:
            self.errorLabelLow.place(relx=0.22,rely=0.94,anchor=tk.CENTER)

            #Reset buttons and exit this function to allow user to try again
            self.startButton.configure(state=NORMAL)
            self.gainBox.config(state=NORMAL)
            self.detectorBox.config(state=NORMAL)
            self.gratingBox.config(state=NORMAL)
            self.stepSlider.config(state=NORMAL)
            self.intSlider.config(state=NORMAL)
            self.extSlider.config(state=NORMAL)
            self.entSlider.config(state=NORMAL)
            self.highEntry.config(state=NORMAL)
            self.lowEntry.config(state=NORMAL)
            self.csv.config(state=NORMAL)
            self.jpg.config(state=NORMAL)
            self.png.config(state=NORMAL)
            self.pltOption.config(state=NORMAL)
            return

        #If the low value IS a number, clear the error
        self.errorLabelLow.place_forget()

        #Check if high value is a number:
        if self.is_number(high)==False:

            #If it isn't, throw an error
            self.errorLabelHigh.place(relx=0.22,rely=0.94,anchor=tk.CENTER)

            #Reset buttons and exit function to allow user to try again
            self.startButton.configure(state=NORMAL)
            self.gainBox.config(state=NORMAL)
            self.detectorBox.config(state=NORMAL)
            self.gratingBox.config(state=NORMAL)
            self.stepSlider.config(state=NORMAL)
            self.intSlider.config(state=NORMAL)
            self.extSlider.config(state=NORMAL)
            self.entSlider.config(state=NORMAL)
            self.highEntry.config(state=NORMAL)
            self.lowEntry.config(state=NORMAL)
            self.csv.config(state=NORMAL)
            self.jpg.config(state=NORMAL)
            self.png.config(state=NORMAL)
            self.pltOption.config(state=NORMAL)
            return

        #If high value was a number, clear the error
        self.errorLabelHigh.place_forget()

        #Check if the low value is larger than the high value
        if float(low) >= float(high):

            #Throw error if it is
            self.highLow.place(relx=0.193,rely=0.94,anchor=tk.CENTER)
       
            #Reset all buttons and exit function to allow user to try again
            self.startButton.configure(state=NORMAL)
            self.gainBox.config(state=NORMAL)
            self.detectorBox.config(state=NORMAL)
            self.gratingBox.config(state=NORMAL)
            self.stepSlider.config(state=NORMAL)
            self.intSlider.config(state=NORMAL)
            self.extSlider.config(state=NORMAL)
            self.entSlider.config(state=NORMAL)
            self.highEntry.config(state=NORMAL)
            self.lowEntry.config(state=NORMAL)
            self.csv.config(state=NORMAL)
            self.jpg.config(state=NORMAL)
            self.png.config(state=NORMAL)
            self.pltOption.config(state=NORMAL)
            return

        #Clear the error if the low value is indeed less than the high value
        self.highLow.place_forget()

        #Check if out of range for 1800 grating
        if grating=='1800 l/mm (Vis)' and (float(high)>869.5875069567 or float(low)<300): #note that at 300 nm you are actually observing 300.0000024nm
            #If out of range, throw error
            self.outOfRange1800.place(relx=0.283,rely=0.94,anchor=tk.CENTER)

            #Reset buttons and exit function to allow user to try again
            self.startButton.configure(state=NORMAL)
            self.gainBox.config(state=NORMAL)
            self.detectorBox.config(state=NORMAL)
            self.gratingBox.config(state=NORMAL)
            self.stepSlider.config(state=NORMAL)
            self.intSlider.config(state=NORMAL)
            self.extSlider.config(state=NORMAL)
            self.entSlider.config(state=NORMAL)
            self.highEntry.config(state=NORMAL)
            self.lowEntry.config(state=NORMAL)
            self.csv.config(state=NORMAL)
            self.jpg.config(state=NORMAL)
            self.png.config(state=NORMAL)
            self.pltOption.config(state=NORMAL)
            return
        
        #Clear the error if the range is okay
        self.outOfRange1800.place_forget()

        #Check if out of range for 600 grating
        if grating=='600 l/mm (IR)' and (float(high)>1000 or float(low)<300):

            #If out of range, throw error
            self.outOfRange600.place(relx=0.23,rely=0.94,anchor=tk.CENTER)

            #Reset buttons and exit function to allow user to try again
            self.startButton.configure(state=NORMAL)
            self.gainBox.config(state=NORMAL)
            self.detectorBox.config(state=NORMAL)
            self.gratingBox.config(state=NORMAL)
            self.stepSlider.config(state=NORMAL)
            self.intSlider.config(state=NORMAL)
            self.extSlider.config(state=NORMAL)
            self.entSlider.config(state=NORMAL)
            self.highEntry.config(state=NORMAL)
            self.lowEntry.config(state=NORMAL)
            self.csv.config(state=NORMAL)
            self.jpg.config(state=NORMAL)
            self.png.config(state=NORMAL)
            self.pltOption.config(state=NORMAL)
            return

        #Clear error for out of range if within range
        self.outOfRange600.place_forget()

        #If the step size is greater than or equal to the range
        if stepSize >= (float(high)-float(low)):

            #Throw error
            self.stepRange.place(relx=0.165,rely=0.94,anchor=tk.CENTER)

            #Reset buttons and exit function to allow user to try again
            self.startButton.configure(state=NORMAL)
            self.gainBox.config(state=NORMAL)
            self.detectorBox.config(state=NORMAL)
            self.gratingBox.config(state=NORMAL)
            self.stepSlider.config(state=NORMAL)
            self.intSlider.config(state=NORMAL)
            self.extSlider.config(state=NORMAL)
            self.entSlider.config(state=NORMAL)
            self.highEntry.config(state=NORMAL)
            self.lowEntry.config(state=NORMAL)
            self.csv.config(state=NORMAL)
            self.jpg.config(state=NORMAL)
            self.png.config(state=NORMAL)
            self.pltOption.config(state=NORMAL)
            return

        #Clear error for too large of step range
        self.stepRange.place_forget()
        if grating=='1800 l/mm (Vis)':
            #Compute the number of data points with the given step size (0.0041666667nm is the step size given by the manual)
            lowStep = int(float(low)/0.0041666667)
            highStep = int(float(high)/0.0041666667)
            rangeDif = highStep-lowStep
            stepLength = int(stepSize/0.0041666667)
            dataPoints = int(rangeDif/stepLength)
        elif grating=='600 l/mm (IR)':
            lowStep = int(float(low)/0.0125)
            highStep = int(float(high)/0.0125)
            rangeDif = highStep-lowStep
            stepLength = int(stepSize/0.0125)
            dataPoints = int(rangeDif/stepLength)
        
        #If exceeding 5000 data points:
        if dataPoints>5000:

            #Throw error if over 5000 data points
            self.dataRange.place(relx=0.215,rely=0.94,anchor=tk.CENTER)

            #Reset buttons and exit function to allow user to try again
            self.startButton.configure(state=NORMAL)
            self.gainBox.config(state=NORMAL)
            self.detectorBox.config(state=NORMAL)
            self.gratingBox.config(state=NORMAL)
            self.stepSlider.config(state=NORMAL)
            self.intSlider.config(state=NORMAL)
            self.extSlider.config(state=NORMAL)
            self.entSlider.config(state=NORMAL)
            self.highEntry.config(state=NORMAL)
            self.lowEntry.config(state=NORMAL)
            self.csv.config(state=NORMAL)
            self.jpg.config(state=NORMAL)
            self.png.config(state=NORMAL)
            self.pltOption.config(state=NORMAL)
            return

        #Clear error for exceeding data point range
        self.dataRange.place_forget()

        #Create progress bar:
        self.progress.place(relx=0.221,rely=0.93,anchor=tk.CENTER)
        self.progress.start()
        self.update()

        #Display message that it is setting...
        self.progressSetting.place(relx=0.221,rely=0.96,anchor=tk.CENTER)
        self.update()

        #Prepare Gain setting:
        if gain=='AUTO':
            gain=4

        if gain=='1x':
            gain=0

        if gain=='10x':
            gain=1
     
        if gain=='100x':
            gain=2

        if gain=='1000x':
            gain=3

        #Prepare mirror setting:
        if detector=='Side':
            detector = 's'

        if detector=='Front':
            detector = 'f'

        #Prepare grating setting:
        if grating=='1800 l/mm (Vis)':
            grating = 'vis'

        if grating=='600 l/mm (IR)':
            grating = 'ir'

        #time.sleep(1)

        #Set the scan parameters for spectrometer, make sure response is good
        response = a.setScanGUI(str(lowStep),str(highStep),str(stepLength),str(intTime),str(int(entSize/12.5)),str(int(extSize/12.5)),str(gain),grating,detector)
        if response==1:
            self.setScanError.place(relx=0.315,rely=0.94,anchor=tk.CENTER)
            return
        
        #Setting complete! Disable message and display that it is starting:
        self.progressSetting.place_forget()
        self.progressScanning.place(relx=0.221,rely=0.96,anchor=tk.CENTER)
        self.update()

        #Start the scan:
        response_start = a.startScan()

        #Check response from spectrometer
        if response_start == 1:
            self.setScanError2.place(relx=0.315,rely=0.94,anchor=tk.CENTER)
            return

        #Done scanning! Disable message and display that it is downloading data
        self.progressScanning.place_forget()
        self.progressData.place(relx=0.221,rely=0.96,anchor=tk.CENTER) 
        self.update()      

        #Get the data
        self.steps,self.intensities = a.getDataScan()

        #Convert steps to nm
        for i in range(len(self.steps)):
            if math.isnan(float(self.steps[i])):
                self.steps[i]=0.0

            grating = self.gratingDefault.get()
            low = float(low)
            if grating == '1800 l/mm (Vis)':
                startingValue = np.round(low/0.0041666667)*0.0041666667
            elif grating == '600 l/mm (IR)':
                startingValue = np.round(low/0.0125)*0.0125

            if grating == '1800 l/mm (Vis)':
                self.steps[i] = float(startingValue) + ((self.steps[i]-1)*float(stepSize))
            elif grating == '600 l/mm (IR)':
                self.steps[i] = float(startingValue) + ((self.steps[i]-1)*float(stepSize))

        #Check for nans (If nan, make it a 0)
        for i in range(len(self.intensities)):
            if math.isnan(float(self.intensities[i])):
                self.intensities[i] = 0.0

        #Convert steps and intensities to float values for accuracy
        self.steps = self.steps.astype('float64')
        self.intensities = self.intensities.astype('float64')

        #Create and display plot:
        self.f = Figure(figsize=(7,5.4),dpi=100)
        self.sample = self.f.add_subplot(111)
        self.sample.plot(self.steps,self.intensities,self.color)
        self.sample.set_title(self.plotTitle)
        self.sample.set_xlabel(self.xlabel)
        self.sample.set_ylabel(self.ylabel)
        self.xmin, self.xmax = self.sample.get_xlim()
        self.ymin, self.ymax = self.sample.get_ylim()

        self.pltcanvas = FigureCanvasTkAgg(self.f,self)
        self.pltcanvas.show()
        self.pltcanvas.get_tk_widget().place(relx=0.72,rely=0.5,anchor=tk.CENTER)
        self.update()

        #Done getting data! Disable message and display new that device is initializing
        self.progressData.place_forget()
        self.progressInit.place(relx=0.221,rely=0.96,anchor=tk.CENTER)
        self.update()

        #Re-initialize spectrometer
        a.initialize()

        #Done with initializing and with progress bar. Clear it all...
        self.progress.place_forget()
        self.progressInit.place_forget()
        self.progress.stop()
        self.update()

        #Reset buttons to allow for new scan
        self.startButton.configure(state=NORMAL)
        self.gainBox.config(state=NORMAL)
        self.detectorBox.config(state=NORMAL)
        self.gratingBox.config(state=NORMAL)
        self.stepSlider.config(state=NORMAL)
        self.intSlider.config(state=NORMAL)
        self.extSlider.config(state=NORMAL)
        self.entSlider.config(state=NORMAL)
        self.highEntry.config(state=NORMAL)
        self.lowEntry.config(state=NORMAL)
        self.csv.config(state=NORMAL)
        self.jpg.config(state=NORMAL)
        self.png.config(state=NORMAL)
        self.pltOption.config(state=NORMAL)
        
#Class for tool options menu
class Tools(tk.Frame):

    def __init__(self,parent,controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)

#Need these to run the app
app = HR460App()
app.mainloop()
