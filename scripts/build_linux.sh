
#!/bin/bash

mkdir ./build
cd ./build
mkdir ./virtual_env

python3 -m venv ./virtual_env

export PATH=$PWD/virtual_env/bin:$PATH

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
python3 -m pip install --upgrade matplotlib
python3 -m pip install --upgrade pyinstaller
python3 -m pip install --upgrade polib

rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/fonts
rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/images
rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/plot_directive
rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/sample_data
rm -Rf ./virtual_env/lib/python*.*/site-packages/matplotlib/mpl-data/stylelib

#pyinstaller --noconfirm --windowed --add-data $PWD/../../assets:assets --icon=$PWD/../../assets/icons/icon.ico ../../VGC_Analyze.py
pyinstaller --onefile --windowed --add-data $PWD/../../assets:assets --icon=$PWD/../../assets/icons/icon.ico --hidden-import='PIL._tkinter_finder' ../../VGC_Analyze.py

