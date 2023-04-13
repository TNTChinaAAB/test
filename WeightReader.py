import Values
import ctypes
import torch
import gzip
import hashlib


def readWeightVersion():
    lib = ctypes.cdll.LoadLibrary("/content/work/data/bins/libnvinfer.so.8")
    NV_VERSION: str = str(lib.getInferLibVersion())
    GPU_NAME: str = torch.cuda.get_device_name(0)
    ID: str = hashlib.sha256(GPU_NAME.encode()).hexdigest()[0:8]
    NUM_THREADS = str(Values.numberThreads)
    with gzip.open("/content/work/data/weights/40b.bin.gz") as _weight_file_:
        Values.MODEL_NAME = str(_weight_file_.readlines()[0]).replace("b'", "").replace("\\n'", "")
    Values.CACHE_NAME = f"trt-{NV_VERSION}_gpu-{ID}_net-{Values.MODEL_NAME}_exact19x19_batch{NUM_THREADS}_fp16"


