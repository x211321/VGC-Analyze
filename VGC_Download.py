
import os
import sys
import shutil
import urllib.parse
import urllib.request
import http.cookiejar
import getpass

from VGC_Var import FILE_PREFIX
from VGC_Img import IMG_CASHE_PATH
from VGC_Img import IMG_CASHE_FRONT
from VGC_Img import IMG_CASHE_BACK
from VGC_Img import IMG_CASHE_CART
from VGC_Img import IMG_COVER_NONE
from VGC_FilePath import writeFile

from VGC_Var import DOWNLOAD_FILE



######################
# downloadCollection
# --------------------   
def downloadCollection(filterData, username = "", password = ""):
    url_base  = "vgcollect.com"
    url_https = "https://" + url_base
    url_auth  = url_https + "/login/authenticate"
    url_csv   = url_https + "/settings/export/collection"
    
    if not filterData.guiMode:
        if len(username) == 0:
            username  = input("Username: ")
        if len(password) == 0:
            password  = getpass.getpass(prompt='Password: ', stream=None)

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
            
                print("\n  Download successful")
                
                # Save downloaded collection data
                writeFile(DOWNLOAD_FILE, contents, "wb")

                filterData.filePath = DOWNLOAD_FILE
            else:
                print("\n  Login error")

                if filterData.guiMode:
                    return "Login error"
                else:
                    sys.exit()
        else:
            print("\n  Error downloading CSV - Code: " + str(response.getcode()))
            
            if filterData.guiMode:
                return "Download error - Code: " + str(response.getcode())
            else:
                sys.exit()
    else:
        print("\n  Login error - Code: " + str(response.getcode()))

        if filterData.guiMode:
            return "Login error - Code: " + str(response.getcode())
        else:
            sys.exit()
        
        
######################
# downloadCovers
# --------------------   
def downloadCovers(itemId, refresh = False, coverType = ""):
    url_base  = "vgcollect.com"
    url_https = "https://" + url_base
    url_front = url_https + "/images/front-box-art/" + str(itemId) + ".jpg"
    url_back  = url_https + "/images/back-box-art/" + str(itemId) + ".jpg"
    url_cart  = url_https + "/images/cart-art/" + str(itemId) + ".jpg"

    if len(coverType) == 0 or coverType == "front":
        downloadCover(itemId, url_front, IMG_CASHE_FRONT, refresh)
    if len(coverType) == 0 or coverType == "back":
        downloadCover(itemId, url_back, IMG_CASHE_BACK, refresh)
    if len(coverType) == 0 or coverType == "cart":
        downloadCover(itemId, url_cart, IMG_CASHE_CART, refresh)


######################
# downloadCover
# --------------------   
def downloadCover(itemId, url, path, refresh):

    itemPath = path + str(itemId) + ".jpg"

    # Check if cover already cashed
    if refresh == False:
        if os.path.exists(itemPath):
            print(itemPath + " already exists")
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
        shutil.copyfile(IMG_COVER_NONE, itemPath)
        pass

