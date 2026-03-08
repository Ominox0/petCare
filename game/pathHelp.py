import os
import sys


def resourcePath(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def savePath(name):
    base = os.path.join(os.getenv("LOCALAPPDATA"), "PetCare", "saves")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, name + ".save")
