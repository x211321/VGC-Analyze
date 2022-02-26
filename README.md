# VGC_Analyze
VGC_Analyze is a graphical data analyzer for your VGCollect.com video game collection.

**VGC_Analyze is an unofficial project, not affiliated with or endorsed by VGCollect.com.**


VGC_Analyze is meant to provide ways to view your collection data from different angels.

Have you ever wondered how much you've spend on your collection, how many imported items you own or what percentage of your collection consists of SEGA products? VGC_Analyze provides answers to all these questions and many more.


# Features
 * Download your collection data from your VGCollect.com profile
 * Sort, filter, group and compare your collection by various attributes
 * Create templates for easy access to often used filter combinations
 * Graph data as a bar, pie, area or line chart
 * Export your collection as a printable HTML page
 * Assign platform holders to specific keywords
 * Combine related platforms for better comparisons
 * Overwrite platform names to achieve a more cohesive data base
 * Expand your collection by settings bookmarks or marking items as completed


# Limitations
VGC_Analyze uses the CSV data that's provided by the VGCollect.com backup function. The data provided this way is rather limited and mostly includes information that's required for restoring a VGCollect.com collection. The data source doesn't include detailed item information like publishers, developers, or release dates and can therefore not be used by VGC_Analyze.

Date and price of purchase as well as the "cart", "box", "manual" and "others" attributes are included in the data, provided you have filled them in.

 * VGC_Analyze can't analyze data that's not there. Depending on the way you maintain your collection the program will be more or less useful to you.

 * VGC_Analyze is not able to query external price charting databases or similar data providers and probably never will be.

 * VGC_Analyze is not a VGCollect.com client. It's not possible to add items to your collection or to create new items in the database. All collection maintenance must be made on the official website.


# Installation
VGC_Analyze is written in Python, using the Tkinter/Tk GUI Toolkit and should thus run on most modern desktop operating systems.

# Windows
There are three ways to run VGC_Analyze on windows.

 * Installer
 * Standalone executable
 * Python script

You can download your preferred version from the [releases page](https://github.com/x211321/VGC_Analyze/releases).

> ⚠ VGC_analyze requires a current version of the [Microsoft Visual C++ redistributable runtime](https://support.microsoft.com/en-us/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0) for its graphing feature. On most machines this should already be installed. Check you system configuration in case of missing graphs.

## Windows - Installer
The windows installer comes bundled with all required dependencies and brings its own Python runtime.


> ⚠ In Windows 10 Microsoft implemented a warning message when an "unrecognized app" is executed for the first time. In this case you have to click on "More info" and confirm with the "Run anyway" button before the installer can be run.


## Windows - Standalone executable
The standalone executable also comes pre bundled with all required dependences and its own Python runtime but can be run without prior installation.

The standalone version is created with [Pyinstaller](https://www.pyinstaller.org/). Pyinstaller combines all files that are required to run a particular Python script into one self extracting archive. When the standalone version is executed Pyinstaller extracts the program data into the windows temp folder and then runs the Python script from there. This behavior can be seen as suspicious by anti-virus software and can cause false security alerts. If you run into trouble running the standalone version, it is recommended that you use the installer instead.


> ⚠ In Windows 10 Microsoft implemented a warning message when an "unrecognised app" is executed for the first time. In this case you have to click on "More info" and confirm with the "Run anyway" button.

## Windows - Python script
Make sure you have a recent version of [Python 3](https://www.python.org/downloads/) installed.

Download the **VGC_Analyze_script.zip** file from the [releases page](https://github.com/x211321/VGC_Analyze/releases) and extract it somewhere on your hard drive.

VGC_Analyze requires a couple third party Python modules that are not included in the zip file. These can be installed via the "package installer for Python" ([pip]([https://pypi.org)). **While the application can be run without those modules, it is recommended that you install them, otherwise certain function will be unavailable.**



```
python -m pip install Pillow
python -m pip install matplotlib
```

 * Pillow is an imaging library providing support for different image formats.
 * Matplotlib provides comprehensive plotting functions


You should now be able to run VGC_Analyze by starting the **VGC_Analyze.py** file from the directory you've extracted the zip file to. Depending on whether you have associated .py files with the Python launcher, you can either double-click the file or run it from a command line.

```
python VGC_Analyze.py
```


# Linux
There are three ways to run VGC_Analyze on Linux.

 * .deb package
 * Standalone executable
 * Python script

You can download your preferred version from the [releases page](https://github.com/x211321/VGC_Analyze/releases).

VGC_Analyze has been tested to run on Ubuntu 20.4 and Linux Mint 20.3.

## Linux - .deb package
For Debian based distributions (Ubuntu, Mint, etc.) a .deb package is provided. Your system's package manager will manage all necessary dependencies. After installation VGC_Analyze should show up in your application launcher under the "Games" section. 

Alternatively run VGC_Analyze from the command line:

```
> vgcanalyze
```

## Linux - Standalone executable
Like the windows version, the standalone executable for Linux comes pre bundled with all required dependences and its own Python runtime and can be run without prior installation.

It might be necessary to set the "execute" permission of the binary file before the standalone version can be run.

```
chmod +x ./VGC_Analyze
./VGC_Analyze
```

If you run into any incompatibilities with the standalone version, it is recommended that you use the script version instead.

## Linux - Python script
Python 3 should already be provided by most Linux distributions.

Download the **VGC_Analyze_script.zip** file from the [releases page](https://github.com/x211321/VGC_Analyze/releases) and extract it somewhere on your hard drive.

The required dependencies can be installed via the package manager.

Debian/Ubuntu/Mint
```
sudo apt-get install python3-tk
sudo apt-get install python3-pil
sudo apt-get install python3-pil.imagetk
sudo apt-get install python3-matplotlib
```

Arch Linux
```
sudo pacman -S tk
sudo pacman -S python-pillow
sudo pacman -S python-matplotlib
```

After that you should be able to start the application by running:
```
python3 ./VGC_Analyze.py
```


# macOS
Currently there is no installer or standalone version of VGC_Analyze for macOS. Your only option is to run the Python script directly.

VGC_Analyze has been tested on macOS Big Sur with Python 3.9.5.

The default version of Python3, that is distributed with macOS, does not work well with VGC_Analyze. It is recommendet that you download and install the latest Version from [python.org](https://python.org).

The rest of the installation process is similar to the other script versions.

Download the **VGC_Analyze_script.zip** file from the [releases page](https://github.com/x211321/VGC_Analyze/releases) and extract it somewhere on your hard drive.

Install the dependencies via [pip]([https://pypi.org).
```
sudo python3 -m pip install Pillow
sudo python3 -m pip install matplotlib
```

Run the script with the python interpreter.
```
python3 ./VGC_Analyze.py
```


# Future development
VGC_Analyze is a hobby project, mostly as a way for us to get to know the Python programming language. Once the basic functionality is implemented the project probably won't be maintained a whole lot.
