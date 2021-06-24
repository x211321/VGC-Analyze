import sys
sys.path.append("../")

from lib.Version import VERSION

# Inno Setup version file
file = open ("setup_windows_version.iss", "w", encoding="utf-8")
file.write("#define MyAppVersion \""+VERSION+"\"")
file.close()

# File name version
file = open ("file_name_version", "w", encoding="utf-8")
file.write(VERSION)
file.close()
