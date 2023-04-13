import WebUtils
import Handler
import FileUtils
import Values
from ShellUtils import *

def download_libnvinfer_deb(version: str, path: str):
    repo = "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64"
    url_ = f"{repo}/libnvinfer8_{version}_amd64.deb"
    isDownloadedFailed = Handler.isProcessFailed(3)
    isEqual = WebUtils.getUrlFileSize(url_) == FileUtils.getFileSize(path)
    if isDownloadedFailed and (not isEqual):
        status = callShell(f"wget {url_} -O {path}")
        FileUtils.chmod_file(path)
        Handler.handle_process(status, "downloaded lib1.deb", "downloading lib1.deb", 3)


def downloadKataGo():
    url_ = "https://github.com/TNTChinaAAB/lib/releases/download/1.0.0/katago"
    size1 = FileUtils.getFileSize("./data/bins/katago")
    size2 = WebUtils.getUrlFileSize(url_)
    if size1 != size2:
        callShell(f"wget \"{url_}\" -O ./data/bins/katago")


def downloadWeights(id_5):
    url_ = WebUtils.getWeightUrl(id_5)
    _status = callShell(f"wget \"{url_}\" -O /content/work/data/weights/40b.bin.gz")
    if _status == 0:
        print("Downloaded " + Values.WEIGHT_FILE + " successfully.")
    else:
        print("There was an error while downloading " + Values.WEIGHT_FILE + ".")

