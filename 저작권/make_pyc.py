import py_compile
import sys
from glob import glob
import shutil
import os

# 파일명 받기 및 pyc 생성
filename = sys.argv[1]
py_compile.compile(filename)

# pyc파일 가져오기
folder_path = os.path.dirname(filename)
filename = os.path.basename(filename).split(".")[0]

pyc_path = glob(os.path.join(folder_path, "__pycache__") + "/" + filename+"*")[0]

# pyc 파일 이동
shutil.move(pyc_path, os.path.join(folder_path, "./%s.pyc"%filename))

# py 파일 이동
shutil.move(os.path.join(folder_path, "./%s.py"%filename), os.path.join(folder_path, "./original", "./%s.py"%filename))

# 원본 pyc 삭제
# os.remove(pyc_path)
