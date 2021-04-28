import os
import sys

languages = ["en", "de"]

pyToolPath = os.path.dirname(sys.executable).replace("\\", "/") + "/tools/"



for language in languages:

    path = "../locales/" + language + "/"

    os.system("\""+pyToolPath + "i18n/msgfmt.py\"  -o "+path+"base.mo " + path+"base")