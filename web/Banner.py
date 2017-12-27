# -*- coding: utf-8 -*-
class Banner:

    def __init__(self):
        self.Version = 0  # 版本信息
        self.Length = 0  # banner长度
        self.Pid = 0  # 进程ID
        self.RealWidth = 0  # 设备的真实宽度
        self.RealHeight = 0  # 设备的真实高度
        self.VirtualWidth = 0  # 设备的虚拟宽度
        self.VirtualHeight = 0  # 设备的虚拟高度
        self.Orientation = 0  # 设备方向
        self.Quirks = 0  # 设备信息获取策略

    def toString(self):
        message = "Banner [Version=" + str(self.Version) + ", length=" + str(self.Length) + ", Pid=" + str(
            self.Pid) + ", realWidth=" + str(self.RealWidth) + ", realHeight=" + str(
            self.RealHeight) + ", virtualWidth=" + str(self.VirtualWidth) + ", virtualHeight=" + str(
            self.VirtualHeight) + ", orientation=" + str(self.Orientation) + ", quirks=" + str(self.Quirks) + "]"
        return message