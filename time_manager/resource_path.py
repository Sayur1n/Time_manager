import os
import sys

def resource_path(relative_path):
    """获取资源文件的路径（兼容开发和打包）"""
    if hasattr(sys, '_MEIPASS'):  # PyInstaller 打包后的临时目录
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")  # 开发环境的目录
    return os.path.join(base_path, relative_path)

def get_writable_folder(foldername):
    """获取可写目录（如当前工作目录下的 music 文件夹）"""
    writable_folder = os.path.join(os.getcwd(), foldername)
    if not os.path.exists(writable_folder):
        os.makedirs(writable_folder)
    return writable_folder