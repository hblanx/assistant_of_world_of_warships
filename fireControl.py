import sys
from getScreen import Screen
sys.path.append("./machineLearning")
from machineLearning.MyYoloClass import *
import time
import base64
import PIL.Image as Image


class FireControl():
    def __init__(self, debug=False):
        self.sc = Screen("./setting.env")
        self.size = 320 # 单张正方形图片长宽高
        self.outSize = 640 #交给yolo的图像长宽高
        self.debug = debug
        self.yolo = MyYolo()
        self.funcType = 3 # 近距离下炮击修正公式类型

    def saveImg(self, image):
        num = random.randint(1, 9999)
        # print(f"debug,saveImg(./img/{num}.jpg)")
        cv2.imwrite(f"./img/{num}.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    def joinImg(self,*args):
        # 接收3个numpy数组图像，返回拼接后的numpy数组图像
        to_image = Image.new('RGB', (self.outSize, self.outSize))  # 创建一个新图
        imgList = map(lambda img: Image.fromarray(np.uint8(img)), args)
        size = [(0, 0), (self.size, 0), (0, self.size)]
        for i, img in enumerate(imgList):
            to_image.paste(img, size[i])
        return np.asarray(to_image)

    # def timer(func):  # 记录计算时间
    #     def wrapped(self,*args,**kwargs):
    #         t1 = time.time()
    #         res = func(self,*args,**kwargs)
    #         t2 = time.time()
    #         with open("tmp.txt", "a") as f:
    #             f.write(str(t2 - t1) + "\n")
    #         return res
    #     return wrapped

    def Qfunc(self, s):
        # 使用拟合结果修正近距离下误差
        # 使用二次函数
        return np.power(s, 2) * 0.08302559 + s * (-1.90135427) + 11.83879507

    def IPfunc(self, s):
        # 使用拟合结果修正近距离下误差
        # 使用反比例函数
        return 1 / s * 26.0585895 - 1.17967778

    def Dfunc(self, s):
        # 使用拟合结果修正近距离下误差
        # 使用推导公式
        return 20 / s

    def getImg(self, hwin, size, fit=True):
        # 根据输入的位置获取图片
        screen = self.sc.getScreen(hwin, size)
        if (not fit):
            return screen
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        screen = cv2.resize(screen, (self.size,self.size), interpolation=cv2.INTER_NEAREST)
        # yolo需要bgr格式，但我训练时使用了灰度化预处理
        # 如果准确度不高，可以考虑消掉下面两行注释取
        # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # screen = cv2.cvtColor(screen, cv2.COLOR_GRAY2RGB)

        # 直接返回image对象
        return screen

    def axis2float(self,data):
        # 获取分类信息并返回float
        info = ""
        data.sort(key=lambda x: x[2][0])
        for num in data:
            if num[0] != 'd':
                info += num[0]
            else:
                info += "."
        try:
            return float(info)
        except:
            print("error,axis2float():", info)
            return -1

    def data2Num(self,data,complex=False):
        # 使用预测信息中的xy坐标轴数据排序成数字
        # complex控制是否对y方向也排序
        if complex:
            # 需要识别两层数字
            up = max(data, key=lambda x: x[2][1])[2][1]
            down = min(data, key=lambda x: x[2][1])[2][1]
            split = (up + down) / 2  # 上下两行的中点
            upList = [] # 存放上下两层数据
            downList = []
            for ele in data:
                if ele[2][1] > split:  # 高度值越大越靠下
                    downList.append(ele)
                else:
                    upList.append(ele)

            down = self.axis2float(downList)
            up = self.axis2float(upList)
            return [up, down]
        else:
            # 只识别一层数字
            return self.axis2float(data)



    def getNum(self, image):
        # 接受numpy数组图片，进行截图返回图中数字
        data = self.yolo.plug(image)
        # 返回值的样式为[['类型', 置信度, (x轴起点, y轴起点, 宽, 高)],...]
        # xy轴左上角为0
        timeList = [] # 时间列表
        sanddList = [] # 速度和距离列表
        thetaList = [] # 角度列表
        for i in range(len(data)-1,-1,-1):
            # 倒序遍历预测结果，将数据分类
            if(data[i][2][0] < 320 and data[i][2][1] < 320):
                timeList.append(data.pop(i))
                continue
            if (data[i][2][0] > 320 and data[i][2][1] < 320):
                sanddList.append(data.pop(i))
                continue
            if (data[i][2][1] > 320):
                thetaList.append(data.pop(i))
                continue
        time = self.data2Num(timeList)
        distance,speed = self.data2Num(sanddList,complex=True)
        theta = self.data2Num(thetaList)
        if self.debug:
            self.saveImg(image)
        return [time,distance,speed,theta]

    def compute(self):
        hwin = self.sc.getHwin()
        # 先进行截图
        timeImg = self.getImg(hwin, self.sc.time)
        sdImg = self.getImg(hwin, self.sc.sd)
        thetaImg = self.getImg(hwin, self.sc.theta)
        finImg = self.joinImg(timeImg,sdImg,thetaImg)

        # 获取训练图片就解开下面2行注释
        # self.saveImg(finImg)
        # return "shot"

        # 获得时间、距离、速度、角度
        time,distance,speed,theta = self.getNum(finImg)
        # 判断时间值是否合法
        if (time < 0 or time > 25):
            self.saveImg(timeImg)
            return "时间数值错误"
        # 判断速度值是否合法
        if (speed < 10 or speed > 80):
            self.saveImg(sdImg)
            return "速度数值错误"
        # 判断距离值是否合法
        if (distance < 0 or distance > 40):
            self.saveImg(sdImg)
            return "距离数值错误"
        # 判断角度值是否合法
        if (theta < 0 or theta > 360):
            self.saveImg(thetaImg)
            return "角度数值错误"

        print(f"debug,time:{time},speed:{speed},theta:{theta}distance:{distance}")
        theta = np.radians(theta)  # 角度转弧度
        # 原公式：对方航速÷20×落弹时间×sin夹角+对方体现在瞄准X轴上船头到核心舱距离
        if (self.funcType == 3):
            # 公式推导全距离可用
            rate = self.Dfunc(distance)
        elif(distance <= 12):
            # 近距离修正
            if(self.funcType == 1):
                rate = self.Qfunc(distance)
            else:
                rate = self.IPfunc(distance)
        else:
            # 不使用修正
            rate = 1
        predict =  rate * speed / 20 * time * np.sin(theta)


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


# if __name__ == '__main__':
#     fc = FireControl(debug=False)
#     print(fc.compute())