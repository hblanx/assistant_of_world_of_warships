import cv2

from getScreen import Screen


class Radar():
    def __init__(self, useBaiduyun=True):
        # 雷达船信息
        self.radarList = {"斯莫兰": 7.5, "奥坎": 7.5, "布莱克": 9.5, "密苏里": 9.5, "塞勒姆": 8.5,
                          "伍斯特": 9, "波多黎各": 10, "得梅因": 10, "阿拉斯加": 10,
                          "水牛城": 10, "西雅图": 9, "威奇塔": 9, "蒙彼利埃": 9, "亚特兰大": 8.5,
                          "印第安纳波利斯": 10, "克利夫兰": 9, "巴尔的摩": 10,
                          "米诺陶": 10, "莫斯科": 12, "恰巴耶夫": 12, "斯大林格勒": 12,
                          "彼得罗巴": 12, "奥恰科夫": 10, "普利茅斯": 9, "海王星": 10, "爱丁堡": 10,
                          "贝尔法斯特": 9, "迪米特里": 12, "喀琅施": 12, "亚历山大": 12, "里加": 12,
                          "塔林": 12, "岳阳": 7.5, "忠武": 7.5, "咸阳": 7.5, "星座": 10}
        self.sc = Screen()
        self.windowSize = (960, 0, 1400, 700)  # 截图位置，根据分辨率而改变，通常这个设置不用改变
        self.useBaiduyun = useBaiduyun  # 是否使用百度云

    def getImg(self):
        # 调用时进行截图，返回cv2图片
        hwin = self.sc.getHwin()
        screen = self.sc.getScreen(hwin, self.windowSize)
        # cv2.imwrite("./test.jpg", screen, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        img = cv2.imencode('.jpg', screen)[1]
        return img

    def getRadarShipList(self, msg):
        # 返回[[雷达船名、雷达距离],...]
        # 第一艘船雷达距离最远
        text = ''
        for s in msg:
            text += s["words"]
        activeList = []  # 场上雷达船列表
        radarList = self.radarList.keys()
        for shipName in radarList:
            if shipName in text:
                activeList.append([shipName, self.radarList[shipName]])
        if (len(activeList) != 0):
            activeList.sort(key=lambda x: x[1], reverse=True)
            return activeList
        else:
            return ["无雷达船", 0]


if __name__ == '__main__':
    r = Radar(False)
    print(r.getRadarShipList())
