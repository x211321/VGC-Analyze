# VGC_Analyze
VGC_Analyze is a graphical data analyzer for your VGCollect.com video game collection.

**VGC_Analyze is an unofficial project, not affiliated with or endorsed by VGCollect.com.**


VGC_Analyze is meant to provide ways to view your collection data from different angels.

Have you ever wondered how much you've spend on your collection, how many imported items you own or what percentage of your collection consists of Sega products? VGC_Analyze provides answers to all these questions and many more.


# Features
 * Download your collection data from your VGCollect.com profile
 * Sort, filter, group and compare your collection by various attributes
 * Chart your collection as a bar, pie, area or line chart
 * Export your collection as a printable HTML page
 * Group your collection by platform holder
 * Combine related platforms for better comparisons
 * Overwrite platform names to achieve a more cohesive data base
 * Expand your collection by settings bookmarks or marking items as completed


# Limitations
VGC_Analyze uses the CSV data that's provided by the VGCollect.com backup function. The data provided this way is rather limited and mostly includes information that's required for restoring a VGCollect.com collection. The data source doesn't include detailed item information like publishers, developers, or release dates and can therefore not be used by VGC_Analyze.

Date and price of purchase as well as the cart, box, manual and "others" attributes are included in the backup data, provided you have filled them in.

 * VGC_Analyze can't analyze data that's not there. Depending on the way you maintain your collection the program will be more or less useful to you.

 * VGC_Analyze is not able to query external price charting databases or similar data providers and probably never will be.

 * VGC_Analyze is not a VGCollect.com client. It's not possible to add items to your collection or to create new items in the database. All collection maintenance must be made on the official website.


# Installation
VGC_Analyze is written in Python, using the Tkinter/Tk GUI Toolkit and should thus run on most modern desktop operating systems.

## Windows
Currently there are two ways to run VGC_Analyze on windows. Provided on this page you'll find a zip file including the raw Python script - which can be run through the Python interpreter - as well as a self containing binary bundle which provides its own Python runtime and all required dependencies.

## Windows - Script version
**Make sure you have a recent version of Python 3 installed.**

https://www.python.org/downloads/

**Download the VGC_Analyze.zip file from this page and extract it somewhere on your hard drive.**

VGC_Analyze requires a couple third party Python modules that are not included in the zip file. These can be installed via the "package installer for Python" (pip).

https://pypi.org

```
python -m pip install Pillow
python -m pip install matplotlib
```

 * Pillow is an imaging library providing support for different image formats.
 * Matplotlib provides comprehensive plotting functions


You should now be able to run VGC_Analyze by starting the **VGC_Analyze.py** file from the directory you've extracted the zip file to. Depending on whether you have associated .py files with the Python launcher or not you can either double-click the file or run it from a command line.

```
python VGC_Analyze.py
```


## Windows - Binary version
The binary version of VGC_Analyze is a standalone bundle containing its own Python runtime as well as all required dependencies like matplot and pillow. Compared to the script version the binary version is much larger but provides the convenience of a self-contained package without any extra setup.

The binary version is created with Pyinstaller (https://www.pyinstaller.org/). Pyinstaller basically packs all files that are required to run a particular Python script into one self extracting archive. When the program is started Pyinstaller extract the archive into the windows temp folder and then runs the Python script from there. This behavior can be seen as suspicious by anti-virus software and can cause false security alerts. If you run into trouble running the binary version it's recommended that you use the script version instead.


Neither the script nor the binary version of VGC_VGC_Analyze must be traditionally "installed". Both versions run directly from the directory to which they were extracted. VGC_Analyze creates sub-folders and files in the directory from which it is run, so to work properly the program should not be placed into a location that's not writable with limited access like "C:\Program Files".



## Linux
VGC_Analyze has been tested to run on Ubuntu 20.4. Currently there is no binary version for Linux so the only way is to run the script version. The steps are similar to the Windows version. Python 3 should already be provided by most Linux distributions and the required dependencies can be installed via the package manager.

```
sudo apt-get install python3-tk
sudo apt-get install python3-pil
sudo apt-get install python3-pil.imagetk
sudo apt-get install python3-matplotlib
```


## macOS
VGC_Analyze has not yet been tested on macOS. Provided the required Python version and dependencies are installed it should theoretically be able to run.


# Future development
VGC_Analyze is a hobby project, mostly as a way for us to get to know the Python programming language. Once the basic functionality is implemented the project probably won't be maintained a whole lot.