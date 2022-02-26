
#!/bin/bash

# Generate and read version info
python3 ./versionInfoGen.py
VERSION=$(<file_name_version)

# Create virual environment
mkdir ./build
cd ./build
mkdir ./virtual_env

python3 -m venv ./virtual_env

# Activate virual environment
export PATH=$PWD/virtual_env/bin:$PATH

# Install dependencies
python3 -m pip install pip
python3 -m pip install Pillow
python3 -m pip install matplotlib
python3 -m pip install pyinstaller
python3 -m pip install polib

# Cleanup dependencies to reduce the file size of the executable
rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/fonts
rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/images
rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/plot_directive
rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/sample_data
rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/stylelib

# Run Pyinstaller for the standalone linux binary
pyinstaller --onefile \
            --windowed \
            --add-data $PWD/../../assets:assets \
            --icon=$PWD/../../assets/icons/icon.ico \
            --hidden-import='PIL._tkinter_finder' \
            --name="VGC_Analyze_${VERSION}_standalone_linux" \
            ../../VGC_Analyze.py
