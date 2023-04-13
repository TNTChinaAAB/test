import os
import Values
import zipfile
import sys
import ctypes
import FileUtils
import WebUtils
import Downloader
from ShellUtils import *


def ensureVersion():
    if Values.WEIGHT_FILE == "auto":
        Values.WEIGHT_FILE = "18b"

    Values.is18b = Values.WEIGHT_FILE == "18b"
    Values.is40b = Values.WEIGHT_FILE == "40b"
    Values.is60b = Values.WEIGHT_FILE == "60b"

    if Values.is18b:
        Values.numberThreads = 24
    elif Values.is60b:
        Values.numberThreads = 16
    elif Values.is40b:
        Values.numberThreads = 12


def handle_configs():
    os.chdir("/content/work")
    pre = "sed -i -e \'s|"
    las = "|g\' ./data/configs/default_gtp.cfg"
    cmd_1 = f"{pre}numSearchThreads =.*|numSearchThreads = {Values.numberThreads}{las}"
    cmd_2 = f"{pre}lagBuffer =.*|lagBuffer = 2.0{las}"
    callShell(cmd_1)
    callShell(cmd_2)


def handleWeight():
    print("Handling Weights...")
    _id_ = ""
    if Values.is18b:
        _id_ = "18b"
    elif Values.is40b:
        _id_ = "40b"
    elif Values.is60b:
        _id_ = "60b"
    else:
        print("Error! Weight file can only choose 40b, 60b and 18b, others are not supported.")
        sys.exit(1)

    if FileUtils.getFileSize("/content/work/data/weights/40b.bin.gz") != WebUtils.getWeightSize(_id_):
        print("Start downloading ", Values.WEIGHT_FILE, "...")
        Downloader.downloadWeights(_id_)


def handleResources():
    if FileUtils.isDirExists("/content/work.zip"):
        callShell("rm -rf /content/work.zip")

    work_zip_url = "https://github.com/TNTChinaAAB/lib/releases/download/1.0.0/work.zip"
    is_work_zip_same = WebUtils.getUrlFileSize(work_zip_url) == FileUtils.getFileSize("/content/work.zip")
    isWorkZipOK = zipfile.is_zipfile("/content/work.zip") and is_work_zip_same
    isWorkDirExist = FileUtils.isDirExists("/content/work")
    isDownloadZipUnsuccessfully = isProcessFailed(1)
    isUnzippedUnsuccessfully = isProcessFailed(2)
    isNeedToUnzip = (not isWorkDirExist) or isUnzippedUnsuccessfully
    isNotExistDirButExistOKWorkZip = isUnzippedUnsuccessfully and isWorkZipOK
    isNeedToDownloadZip = (not isNotExistDirButExistOKWorkZip) and (
            ((not isWorkZipOK) and FileUtils.isFileExists("/content/work.zip")) or isDownloadZipUnsuccessfully)

    if (isNeedToUnzip and (not isWorkZipOK)) or isNeedToDownloadZip:
        print("Downloading work.zip...")
        status1 = callShell(f"wget \"{work_zip_url}\" -O /content/work.zip")
        FileUtils.chmod_file("/content/work.zip")
        handle_process(status1, "downloaded work.zip", "downloading work.zip", 1)
    if zipfile.is_zipfile("/content/work.zip") and isNeedToUnzip:
        print("Unzip work.zip...")
        status2 = callShell("unzip -o /content/work.zip -d /content/")
        handleUnzipped(status2)


def unpacking_deb(dir_: str, lib1_path: str, targetDir: str):
    if FileUtils.isFileExists(lib1_path) and (not isProcessFailed(3)):
        callShell(f"mkdir -p {dir_}/extract")
        cmd_1 = f"dpkg -X {lib1_path} {dir_}/extract"
        cmd_2 = f"cp -rf {dir_}/extract/usr/lib/x86_64-linux-gnu/. {targetDir}"
        callShell(f"{cmd_1} && {cmd_2}")
        FileUtils.chmod_file(f"{targetDir}")
        callShell(f"rm -rf {lib1_path}")
        callShell(f"rm -rf {dir_}/extract")


def check_libnvinfer_so():
    dir_ = "/root/byTNTChina"
    lib1_path = f"{dir_}/lib1.deb"
    target_path = "/content/work/data/bins/libnvinfer.so.8"
    target_dir = "/content/work/data/bins"
    try:
        ctypes.cdll.LoadLibrary(target_path)
    except OSError as e_1:
        Downloader.download_libnvinfer_deb(Values.LIBNVINFER_VERSION, lib1_path)
        unpacking_deb(dir_, lib1_path, target_dir)


def isProcessFailed(code: int) -> int:
    a = FileUtils.isFileExists(f"/root/byTNTChina/error{code}.txt")
    b = not FileUtils.isFileExists(f"/root/byTNTChina/success{code}.txt")
    return a or b


def handle_process(status: int, smg: str, emg: str, code: int):
    if status == 0:
        print(f"Successfully {smg}.")
        if FileUtils.isFileExists("/root/byTNTChina/error1.txt"):
            callShell(f"rm -rf /root/byTNTChina/error{code}.txt")
        callShell(f"echo '{code}' > /root/byTNTChina/success{code}.txt")
    else:
        print(f"There was an error while {emg}. Please contant with the jupter notebook's author.")
        callShell(f"echo '{code}'> /root/byTNTChina/error{code}.txt")
        sys.exit(1)


def handleUnzipped(statusA: int):
    if statusA == 0:
        callShell("rm -rf /content/work.zip")
    handle_process(statusA, "unzipped work.zip", "unzipping work.zip", 2)
