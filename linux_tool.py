import os


# 计算磁盘剩余（单位：G）
def cal_device_left(folder):
    st = os.statvfs(folder)
    return st.f_bavail * st.f_frsize / 1024 / 1024 / 1024

