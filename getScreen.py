import json

import numpy as np
import win32api
import win32con
import win32gui
import win32ui


class Screen():
    # 使用getHwin获取当前截图
    def __init__(self, path="setting.env"):
        with open(path, "r") as f:
            data = json.load(f)
        self.time = data["time"]
        self.sd = data["speed_and_distance"]
        self.theta = data["theta"]
        self.path = path

    def getHwin(self):
        return win32gui.GetDesktopWindow()  # 获得句柄

    def getScreen(self, hwin, region=None):
        # 接受win32api截屏，进行裁剪后返回bitmap对象
        if region:
            left, top, width, height = region
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (height, width, 4)

        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return img

    def save(self):
        # 保存
        with open(self.path, "w") as f:
            f.write(json.dumps({
                "time": self.time,  # 落弹时间
                "speed_and_distance": self.sd,  # 目标最大速度
                "theta": self.theta  # 目标角度
            }))

    def modify(self, imageType, incr, toward):
        # print("debug",imageType,incr)
        # 接受图片类型和增量，对数据进行操作
        # imageType:1.落弹时间,2.速度和距离,3.目标夹角
        # toward:1.左边界,2.上边界,3.宽度,4.高度
        if (imageType == 1):
            self.time[toward] += incr
        elif (imageType == 2):
            self.sd[toward] += incr
        elif (imageType == 3):
            self.theta[toward] += incr
        return
