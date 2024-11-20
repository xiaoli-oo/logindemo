import os

# 获取当前文件所在的绝对路径
current_file_path = os.path.abspath(__file__)
print(current_file_path)
# 获取当前文件所在的目录
current_dir = os.path.dirname(current_file_path)

print(current_dir)
from pathlib import Path

# 获取当前文件所在的目录
current_dir = Path(__file__).resolve().parent

print(current_dir)
