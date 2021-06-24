
REM Create virual environment
mkdir .\build
cd .\build
mkdir .\virtual_env

python -m venv .\virtual_env

REM Activate virual environment
set PATH=%CD%\virtual_env\Scripts;%PATH%

REM Install dependencies
python -m pip install pip
python -m pip install Pillow
python -m pip install matplotlib
python -m pip install pyinstaller
python -m pip install polib

REM Cleanup dependencies to reduce the file size of the executable
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\fonts
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\images
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\plot_directive
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\sample_data
rmdir /S /Q .\virtual_env\Lib\site-packages\matplotlib\mpl-data\stylelib

REM Run Pyinstaller

REM Standalone binary
pyinstaller --onefile ^
            --windowed ^
            --add-data="%CD%\..\..\assets;assets" ^
            --icon="%CD%\..\..\assets\icons\icon.ico" ^
            --name="VGC_Analyze_standalone_win" ^
            ..\..\VGC_Analyze.py

REM Bundle for Inno setup installer
pyinstaller --noconfirm ^
            --windowed ^
            --add-data="%CD%\..\..\assets;assets" ^
            --icon="%CD%\..\..\assets\icons\icon.ico" ^
            ..\..\VGC_Analyze.py

REM Generate installer
REM The INNO_SETUP_HOME environment variable must point to
REM the local Inno Setup installation
cd ..
"%INNO_SETUP_HOME%\ISCC.exe" .\setup_windows.iss
