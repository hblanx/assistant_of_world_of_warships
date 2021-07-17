import os

import cv2

from getScreen import Screen


class Map():
    # 教程数据来自于https://www.bilibili.com/read/cv85224/，仅供参考
    # 各个服务器地图名称不同，此功能仅在亚服测试
    def __init__(self):
        self.sc = Screen()
        # 地图名称截图位置，根据分辨率而改变，通常这个设置不用改变
        # left, top, width, height
        self.windowSize = (600, 800, 700, 280)
        # dirPath的路径存放地图攻略图片
        self.dirPath = r"./static/img/map"
        # 文件名称就是地图名称(自动去掉文件后缀),可以往里面更换内容
        dirList = os.listdir(self.dirPath)
        self.mapList = list(map(lambda x: x.split(".")[0], dirList))

    def getImg(self):
        # 获取截图，返回cv2图像
        hwin = self.sc.getHwin()
        image = self.sc.getScreen(hwin, self.windowSize)
        image = cv2.imencode('.jpg', image)[1]
        return image

    def getPath(self, msg):
        # 接收response信息，返回(该指南的图片路径,状态码)
        # 状态码为1时找到攻略，为0时没找到攻略
        text = ''
        for s in msg:
            text += s["words"]
        # print("debug,text:",text)
        # text = "隔海相望震中00:22开始战斗" # 假数据
        for map in self.mapList:
            if (map in text):
                return self.dirPath + "/" + map + ".jpg", 1
        else:
            return "", 0


if __name__ == '__main__':
    mp = Map()
    import time
    from baiduAPI import BaiduAPI

    time.sleep(5)
    bd = BaiduAPI()
    image = mp.getImg()
    msg = bd.ocr(image)
    path, state = mp.getPath(msg)
    responseData = {
        "state": state,
        "path": path
    }
    print(responseData)
