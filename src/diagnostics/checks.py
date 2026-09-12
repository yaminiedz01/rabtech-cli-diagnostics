import os
import shutil
import sys


def check_python_version():
    return {
        "python_version": sys.version.split()[0],
        "executable": sys.executable,
    }


def check_disk_space():
    total, used, free = shutil.disk_usage(os.getcwd())

    return {
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2),
    }


def check_environment():
    return {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("USERPROFILE", ""),
    }