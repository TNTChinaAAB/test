import urllib
import os
import requests
import base64


def getWeightSize(id_2: str) -> int:
    return getUrlFileSize(getWeightUrl(id_2))


def getWeightUrl(id_3: str) -> str:
    return f"https://github.com/TNTChinaAAB/lib/releases/download/1.0.0/{id_3}.bin.gz"


def getUrlFileSize(url: str) -> int:
    return int(urllib.request.urlopen(url).headers['Content-Length'])


def getGoogleFileSize(id1: str) -> int:
    id2: str = "https://drive.google.com/uc?id=" + id1
    return getUrlFileSize(id2)


def get_content(file_path):
    with open(file_path, 'rb') as f:
        f_data = f.read()
        data_b64 = base64.b64encode(f_data).decode('utf-8')  # 将二进制文件编码后转换为字符串形式
        return data_b64


def upload_file(file_path: str, repo_name: str, token: str):
    filename = os.path.split(file_path)[1]
    content = get_content(file_path)
    url_ = "https://api.github.com/repos/{}/contents/{}".format(repo_name, filename)
    headers_ = {
        "Authorization": "token " + token,
        "Content-type": "application/vnd.github+json"
    }
    data_ = {
        "message": f"upload {filename}",
        "content": content
    }

    req = requests.put(url=url_, json=data_, headers=headers_)
