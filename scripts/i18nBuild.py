import os
import sys

languages = ["en_US", "de_DE"]

pyToolPath = os.path.dirname(sys.executable).replace("\\", "/") + "/tools/"



for language in languages:

    path = "../locales/" + language + "/LC_MESSAGES/"

    os.system("\""+pyToolPath + "i18n/msgfmt.py\"  -o "+path+"base.mo " + path+"base")