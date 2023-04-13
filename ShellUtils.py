import subprocess


def callShell(cmd: str) -> int:
    return subprocess.call(cmd, shell=True)


def popenShell(cmd: str) -> subprocess.Popen:
    return subprocess.Popen(args=cmd, shell=True)
