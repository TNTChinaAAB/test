import argparse
import os
import Values
import torch
import sys
import Handler
import FileUtils
import WeightReader
import Caches
import Downloader
from ShellUtils import *

if __name__ == '__main__':
    if not torch.cuda.is_available():
        print("Sorry, your current status has no gpus! You can't run katago.")
        sys.exit(0)
    message = "This is a tool for staring ikatago-server on colab"
    parse = argparse.ArgumentParser(description=message)
    parse.add_argument("--username", type=str, required=True, help="the username of your ikatago-server.")
    parse.add_argument("--password", type=str, required=True, help="The password of your ikatago-server.")
    parse.add_argument("--weight", type=str, required=True, help="The type of your katago weight.")
    parse.add_argument("--frpc", type=str, default=Values.FRPC_DEFAULT, help="The frpc that you custom.")
    args = parse.parse_args()
    Values.USERNAME = args.username
    Values.PASSWORD = args.password
    Values.WEIGHT_FILE = args.weight
    Values.WEIGHT_FILE = Values.WEIGHT_FILE.lower()
    Values.FRPC = args.frpc
    Handler.ensureVersion()
    callShell("mkdir -p /root/byTNTChina")
    callShell("mkdir -p /root/.katago")
    callShell("mkdir -p /root/.katago/trtcache")
    os.chdir("/content/")
    Handler.handleResources()
    callShell("mkdir -p /content/work/data/weights")
    Handler.handleWeight()
    FileUtils.chmod_file("/content/work/data/weights/40b.bin.gz")
    Handler.check_libnvinfer_so()
    WeightReader.readWeightVersion()
    os.chdir("/root/.katago/trtcache/")
    Caches.onInit()
    os.chdir("/content/work")
    Handler.handle_configs()
    Downloader.downloadKataGo()
    FileUtils.chmod()
    callShell(f"echo {Values.USERNAME}:{Values.PASSWORD} > ./userlist.txt")
    callShell(f"echo \"\"\"{Values.FRPC}\"\"\" > config/frpc.txt")
    callShell(f"./change-frpc.sh {Values.USERNAME}")
    callShell("./change-config.sh \'40b\' \'./data/weights/40b.bin.gz\'")
    p1 = popenShell(f"./ikatago-server --platform colab --token {Values.PLATFORM_TOKEN}")
    try:
        p1.wait()
    except KeyboardInterrupt as e:
        print("The progress is closing, don't stop it again.")
        print("Closing...")
        os.chdir("/root/.katago/trtcache")
        Caches.onPost()


