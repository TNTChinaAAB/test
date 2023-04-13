import json
import Values
import FileUtils
import WebUtils
import urllib
from ShellUtils import *


def onInit():
    print("Handling caches...")
    url_ = "https://api.github.com/repos/TNTChinaAAB/KataGo_Caches/contents"
    request_ = urllib.request.urlopen(url_)
    json_ = json.loads(request_.read())
    contain: bool = False
    size: int = 0
    file_size = FileUtils.getFileSize(f"./{Values.CACHE_NAME}")
    download_url = ""
    isCacheExists = FileUtils.isFileExists(f"./{Values.CACHE_NAME}")
    for i in json_:
        if i["name"] == Values.CACHE_NAME:
            contain = True
            size = i["size"]
            download_url = i["download_url"]
    if isCacheExists:
        if contain:
            if file_size != size:
                callShell(f"wget '{download_url}' -O ./{Values.CACHE_NAME}")
        else:
            if file_size != 0:
                print(f"Uploading {Values.CACHE_NAME}...")
                WebUtils.upload_file(f"/root/.katago/trtcache/{Values.CACHE_NAME}", "TNTChinaAAB/KataGo_Caches",
                                     Values.TDG_ATS)  # TODO: 上传文件到仓库
                print("Uploaded successfully!")
    else:
        if contain:
            callShell(f"wget '{download_url}' -O ./{Values.CACHE_NAME}")


def onPost():
    url_ = "https://api.github.com/repos/TNTChinaAAB/KataGo_Caches/contents"
    request_ = urllib.request.urlopen(url_)
    json_ = json.loads(request_.read())
    contain: bool = False
    file_size = FileUtils.getFileSize(f"./{Values.CACHE_NAME}")
    isCacheExists = FileUtils.isFileExists(f"./{Values.CACHE_NAME}")
    for i in json_:
        if i["name"] == Values.CACHE_NAME:
            contain = True
    if isCacheExists:
        if not contain:
            if file_size != 0:
                print(f"Uploading {Values.CACHE_NAME}...")
                WebUtils.upload_file(f"/root/.katago/trtcache/{Values.CACHE_NAME}", "TNTChinaAAB/KataGo_Caches",
                                     Values.TDG_ATS)  # TODO: 上传文件到仓库
                print("Uploaded successfully!")
