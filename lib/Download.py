from lib.Locale import _

import os
import urllib.parse
import urllib.request
import http.cookiejar

import lib.Var as VAR

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

    try:
        request  = urllib.request.Request(url_auth, binary_data, headers)
        response = urllib.request.urlopen(request)

        if response.getcode() == 200:
            request  = urllib.request.Request(url_csv, binary_data, headers)
            response = urllib.request.urlopen(request)
            if response.getcode() == 200:
                contents = response.read()

                if "\"VGC id\"" in str(contents[0:10]):
                    # Save downloaded collection data
                    writeFile(VAR.DOWNLOAD_FILE, contents, "wb")

                    return None, VAR.DOWNLOAD_FILE
                else:
                    return _("Login error"), ""
            else:
                return _("Download error - Code: ") + str(response.getcode()), ""
        else:
            return _("Login error - Code: ") + str(response.getcode()), ""
    except urllib.error.URLError as err:
        try:
            return _("Network error: ") + err.reason, ""
        except:
            return _("Network error"), ""
    except urllib.error.HTTPError as err:
        try:
            return _("Network error: ") + str(err.code) + " " + err.reason, ""
        except:
            return _("Network error"), ""
    except:
        return _("Network error"), ""


######################
# downloadCover
# --------------------
def downloadCover(item, coverType, refresh = False):
    itemId    = item.VGC_id

    url_base  = "vgcollect.com"
    url_https = "https://" + url_base

    url_cover = url_https + "/images/"+coverType+"-art/" + str(itemId) + ".jpg"

    cache     = VAR.IMG_CACHE_PATH + coverType + "/"

    itemPath = cache + str(itemId) + ".jpg"

    # Check if cover already cached
    if refresh == False:
        if os.path.exists(itemPath) or item.getLocalData("missingCover" + coverType):
            print("Skip download for " + itemPath)
            return

    # Create request
    request = urllib.request.Request(url_cover)

    # Check if target path exists
    if os.path.exists(cache) == False:
        os.makedirs(cache)

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
