
REM Create virual environment
mkdir .\build
cd .\build
mkdir .\virtual_env

python -m venv .\virtual_env

REM Activate virual environment
SET PATH=%CD%\virtual_env\Scripts;%PATH%

REM Install dependencies
python -m pip install --upgrade pip
python -m pip install --upgrade Pillow
python -m pip install --upgrade matplotlib
python -m pip install --upgrade pyinstaller
python -m pip install --upgrade polib

REM Cleanup dependencies
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\fonts
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\images
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\plot_directive
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\sample_data
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\stylelib

@REM pyinstaller --onefile --windowed ..\..\VGC_Analyze.py
pyinstaller ..\..\VGC_Analyze.py