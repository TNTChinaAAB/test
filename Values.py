import base64

LIBNVINFER_VERSION = "8.5.3-1+cuda11.8"
numberThreads = 24
CACHE_NAME = ""
MODEL_NAME = ""
USERNAME = ""
PASSWORD = ""
is18b = True
is40b = False
is60b = False
WEIGHT_FILE = ""
FRPC = ""
FRPC_DEFAULT = """
### YOUR FRPC CONTENT ###

[common]
tls_enable = true
server_addr = {{ .Envs.KNAT_SERVER_ADDR }}
server_port = {{ .Envs.KNAT_SERVER_PORT }}
token = {{ .Envs.KNAT_SERVER_TOKEN }}

[kinfkong-ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 2222
remote_port = 0

### END YOUR FRPC CONTENT ###
"""
PLATFORM_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhRW5jcnlwdEtleVByZWZpeCI6ImpibGtqbGF4IiwiaWF0IjoxNjIyNzg4NTg5LCJleHAiOjE5NDg1NzkxOTksImF1ZCI6ImNvbGFiIiwiaXNzIjoia2luZmtvbmcifQ.WMPaTYJAuGx1QbUTrag5eX0e8pVU4eXCxoNlX4h2wrpOV3dMPSfi4boQvUkeAWreWsehNd9o7OxvdGpNQ0r8bIBLITVgoBDTGVTjxrJRrHCIgMa08HIohgwTjInW8SuPNZGFsKrUUnwAqCgS-6VDmc5TKd-t56DJyH6m3I0ELv26jjF7OzlhrSKlIz9HwYxh3OyU1qbsYaKQx74vs1ykacAvHJ4DQETxMmJPLpMOOmA9L7r26Qc8iFXcS5HEaDj-nZDUM471itIHT91QtgjPm9kdSVsO3k20MrOmerB0TM-gVxnEjEyjCfZGwdgGnbfYthBw96QbA6Mhwbf7ipXtlw'
CPJ = "Z2hwX3h3ZmdFa2NETjRHVXkwYU43YlZ2MURZTHcwM2FCRTN6d0t5Zg=="
TDG_ATS = str(base64.b64decode(CPJ), encoding="utf-8")
