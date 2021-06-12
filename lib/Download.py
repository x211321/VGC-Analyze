from lib.Locale import _

import os
import sys
import shutil
import urllib.parse
import urllib.request
import http.cookiejar
import getpass

from lib.Var import FILE_PREFIX
from lib.Var import IMG_CACHE_PATH
from lib.Var import IMG_CACHE_FRONT
from lib.Var import IMG_CACHE_BACK
from lib.Var import IMG_CACHE_CART
from lib.Var import DOWNLOAD_FILE

from lib.FilePath import writeFile


######################
# downloadCollection
# --------------------
def downloadCollection(username = "", password = ""):
    url_base  = "vgcollect.com"
    url_https = "https://" + url_base
    url_auth  = url_https + "/login/authenticate"
    url_csv   = url_https + "/settings/export/collection"

    headers={"Content-Type":"application/x-www-form-urlencoded",
             "User-agent":"Mozilla/5.0 Chrome/81.0.4044.92",    # Chrome 80+ as per web search
             "Host":url_base,
             "Origin":url_https,
             "Referer":url_https}

    cookie_jar = http.cookiejar.CookieJar()
    opener     = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    urllib.request.install_opener(opener)

    payload = {
        'username':username,
        'password':password
    }

    data        = urllib.parse.urlencode(payload)
    binary_data = data.encode('UTF-8')

    request  = urllib.request.Request(url_auth, binary_data, headers)
    response = urllib.request.urlopen(request)

    if response.getcode() == 200:
        request  = urllib.request.Request(url_csv, binary_data, headers)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            contents = response.read()

            if "\"VGC id\"" in str(contents[0:10]):
                # Save downloaded collection data
                writeFile(DOWNLOAD_FILE, contents, "wb")

                return None, DOWNLOAD_FILE
            else:
                return _("Login error"), ""
        else:
            return _("Download error - Code: ") + str(response.getcode()), ""
    else:
        return _("Login error - Code: ") + str(response.getcode()), ""


######################
# downloadCovers
# --------------------
def downloadCovers(item, refresh = False, coverType = ""):
    itemId = item.VGC_id

    url_base  = "vgcollect.com"
    url_https = "https://" + url_base
    url_front = url_https + "/images/front-box-art/" + str(itemId) + ".jpg"
    url_back  = url_https + "/images/back-box-art/" + str(itemId) + ".jpg"
    url_cart  = url_https + "/images/cart-art/" + str(itemId) + ".jpg"

    if len(coverType) == 0 or coverType == "front":
        downloadCover(item, url_front, IMG_CACHE_FRONT, refresh, "Front")
    if len(coverType) == 0 or coverType == "back":
        downloadCover(item, url_back, IMG_CACHE_BACK, refresh, "Back")
    if len(coverType) == 0 or coverType == "cart":
        downloadCover(item, url_cart, IMG_CACHE_CART, refresh, "Cart")


######################
# downloadCover
# --------------------
def downloadCover(item, url, path, refresh, coverType):
    itemId = item.VGC_id

    itemPath = path + str(itemId) + ".jpg"

    # Check if cover already cached
    if refresh == False:
        if os.path.exists(itemPath) or item.getLocalData("missingCover" + coverType):
            print("Skip download for " + itemPath)
            return

    # Create request
    request = urllib.request.Request(url)

    # Check if target path exists
    if os.path.exists(path) == False:
        os.makedirs(path)

    try:
        # Download cover
        response = urllib.request.urlopen(request)

        if response.getcode() == 200:
            print("\n  Download successful - "+ itemPath)
            contents = response.read()

            file = open(itemPath, "wb")
            file.write(contents)
            file.close()
    except:
        item.localData["missingCover"+coverType] = "Yes"
        pass
