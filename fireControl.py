import sys

from getScreen import Screen

sys.path.append("./machineLearning")
from machineLearning.MyYoloClass import *
# import cv2
# import random
import base64


class FireControl():
    def __init__(self, debug=False):
        self.sc = Screen("./setting.env")
        self.size = (640, 640)
        self.debug = debug
        self.yolo = MyYolo()

    def saveImg(self, image):
        num = random.randint(1, 9999)
        # print(f"debug,saveImg(./img/{num}.jpg)")
        cv2.imwrite(f"./img/{num}.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    def getImg(self, hwin, size, fit=True):
        screen = self.sc.getScreen(hwin, size)
        if (not fit):
            return screen
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        screen = cv2.resize(screen, self.size, interpolation=cv2.INTER_NEAREST)
        # yolo需要bgr格式，但我训练时使用了灰度化预处理
        # 如果准确度不高，可以考虑消掉下面两行注释取
        # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # screen = cv2.cvtColor(screen, cv2.COLOR_GRAY2RGB)

        # 直接返回image对象
        return screen

    def getNum(self, image, complex=False):
        # 接受类型，进行截图返回图中数字
        if complex:
            num = self.yolo.plug(image, complex=True)
        else:
            num = self.yolo.plug(image)[0]
        # print("debug,num:",num")
        if self.debug:
            self.saveImg(image)
        return num

    def closeRangeFix(self, s):
        # 使用拟合结果修正近距离下误差
        return np.power(s, 2) * 0.08302559 + s * (-1.90135427) + 11.83879507

    def compute(self):
        hwin = self.sc.getHwin()
        # 先进行截图
        timeImg = self.getImg(hwin, self.sc.time)
        sdImg = self.getImg(hwin, self.sc.sd)
        thetaImg = self.getImg(hwin, self.sc.theta)
        # 获得时间值
        time = self.getNum(timeImg)
        # 判断时间值是否合法
        if (time < 0 or time > 25):
            self.saveImg(timeImg)
            return "时间数值错误"
        # 获得距离和速度
        distance, speed = self.getNum(sdImg, True)
        if (speed < 10 or speed > 80):
            self.saveImg(sdImg)
            return "速度数值错误"
        if (distance < 0 or distance > 40):
            self.saveImg(sdImg)
            return "距离数值错误"
        # 获得角度
        theta = self.getNum(thetaImg)
        if (theta < 0 or theta > 360):
            self.saveImg(thetaImg)
            return "角度数值错误"

        # print(f"debug,time:{time},speed:{speed},theta:{theta}distance:{distance}")
        theta = np.radians(theta)  # 角度转弧度
        if (distance < 12):
            rate = self.closeRangeFix(distance)
            print(f"debug,rate:{rate}")
        else:
            rate = 1

        # 原公式：对方航速÷20×落弹时间×sin夹角+对方体现在瞄准X轴上船头到核心舱距离
        predict = rate * speed / 20 * time * np.sin(theta)
        # print("f"debug,predict:{predict}")
        return np.round(predict, 1)

    def testImg(self, imageType):
        # 测试图片位置是否正确，返回base64编码图片
        hwin = self.sc.getHwin()
        if (imageType == 1):
            screen = self.getImg(hwin, self.sc.time, False)
        elif (imageType == 2):
            screen = self.getImg(hwin, self.sc.sd, False)
        elif (imageType == 3):
            screen = self.getImg(hwin, self.sc.theta, False)
        else:
            return 0
        screen = cv2.imencode('.jpg', screen)[1].tostring()
        return base64.b64encode(screen)


if __name__ == '__main__':
    fc = FireControl(debug=False)
    print(fc.compute())
