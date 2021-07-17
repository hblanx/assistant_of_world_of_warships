import cv2
import numpy as np
import torch
from models.experimental import attempt_load
from numpy import random
from utils.general import check_img_size, non_max_suppression, scale_coords, \
    set_logging
from utils.torch_utils import select_device


class MyYolo():
    def __init__(self):
        # 设置
        self.weights = r'./machineLearning/pt/availableModel.pt'
        self.opt_device = ''  # device = 'cpu' or '0' or '0,1,2,3'
        self.imgsz = 640
        self.opt_conf_thres = 0.3
        self.opt_iou_thres = 0.3

        # Initialize
        set_logging()
        self.device = select_device(self.opt_device)
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA

        # 读取模型
        self.model = attempt_load(self.weights, map_location=self.device)  # load FP32 model
        self.imgsz = check_img_size(self.imgsz, s=self.model.stride.max())  # check img_size
        if self.half:
            self.model.half()  # to FP16

        # Get names and colors
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]

    def letterbox(self, img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True):
        # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
        shape = img.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better test mAP)
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, 32), np.mod(dh, 32)  # wh padding
        elif scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return img, ratio, (dw, dh)

    def predict(self, im0s):
        # Run inference
        img = torch.zeros((1, 3, self.imgsz, self.imgsz), device=self.device)  # init img
        _ = self.model(img.half() if self.half else img) if self.device.type != 'cpu' else None  # run once

        # Set Dataloader & Run inference
        img = self.letterbox(im0s, new_shape=self.imgsz)[0]
        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        # pred = model(img, augment=opt.augment)[0]
        pred = self.model(img)[0]

        # Apply NMS
        pred = non_max_suppression(pred, self.opt_conf_thres, self.opt_iou_thres)

        # Process detections
        ret = []
        for i, det in enumerate(pred):  # detections per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    label = f'{self.names[int(cls)]}'
                    prob = round(float(conf) * 100, 2)  # round 2
                    xywh = xyxy
                    x = (int(xywh[0]) + int(xywh[2])) / 2
                    y = (int(xywh[1]) + int(xywh[3])) / 2
                    w = (int(xywh[2]) - int(xywh[0]))
                    h = (int(xywh[3]) - int(xywh[1]))
                    position = (x, y, w, h)
                    ret_i = [label, prob, position]
                    ret.append(ret_i)
                    # print('found:', x, y, w, h, label)
        # print(ret)
        return ret

    def predict_path(self, path):
        # Run inference
        img = torch.zeros((1, 3, self.imgsz, self.imgsz), device=self.device)  # init img
        _ = self.model(img.half() if self.half else img) if self.device.type != 'cpu' else None  # run once

        # Set Dataloader & Run inference
        im0s = cv2.imread(path)  # BGR
        img = self.letterbox(im0s, new_shape=self.imgsz)[0]
        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        # pred = model(img, augment=opt.augment)[0]
        pred = self.model(img)[0]

        # Apply NMS
        pred = non_max_suppression(pred, self.opt_conf_thres, self.opt_iou_thres)

        # Process detections
        ret = []
        for i, det in enumerate(pred):  # detections per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    label = f'{self.names[int(cls)]}'
                    prob = round(float(conf) * 100, 2)  # round 2
                    xywh = xyxy
                    x = (int(xywh[0]) + int(xywh[2])) / 2
                    y = (int(xywh[1]) + int(xywh[3])) / 2
                    w = (int(xywh[2]) - int(xywh[0]))
                    h = (int(xywh[3]) - int(xywh[1]))
                    position = (x, y, w, h)
                    ret_i = [label, prob, position]
                    ret.append(ret_i)
                    # print('found:', x, y, w, h, label)
        # print(ret)
        return ret

    def getFloat(self, data):
        # 获取分类信息并返回float
        info = ""
        data.sort(key=lambda x: x[2][0])
        for num in data:
            if num[0] != 'd':
                info += num[0]
            else:
                info += "."
        # print("debug,info:",info)
        try:
            return float(info)
        except:
            return -1

    # 在这里编辑接口代码
    def plug(self, im0s, complex=False):
        # 接受image，返回[第一层数字的float,第二层...]
        # debug
        # im0s = cv2.imread("./img/speed591.jpg")  # BGR
        # data的样式为[['3', 89.99, (463.5, 349.0, 161, 370)], ['3', 93.55, (231.0, 348.0, 170, 380)]]
        data = self.predict(im0s)
        # print("debug,data:",data)
        if complex:
            # 需要识别两层数字
            dList = []
            for i in range(len(data) - 1, -1, -1):
                # 反向遍历将小数点先取出来
                if (data[i][0] == 'd'):
                    dList.append(data.pop(i))
            # up是['class',可信度,[坐标]]的列表
            up = max(data, key=lambda x: x[2][1])[2][1]
            down = min(data, key=lambda x: x[2][1])[2][1]
            split = (up + down) / 2  # 上下两行的分割线
            upList = []
            downList = []
            for ele in data:
                if (ele[2][1] > split):  # 高度值越大越靠下
                    downList.append(ele)
                else:
                    upList.append(ele)
            if (len(dList) == 1):
                # 为小数点分层，不过航速似乎没有小数点
                upList.append(dList[0])
            else:
                dList.sort(key=lambda x: x[2][1])
                upList.append(dList[-1])
                downList.append(dList[0])
            down = self.getFloat(downList)
            up = self.getFloat(upList)
            return [up, down]

        else:
            # 只识别一层数字
            return [self.getFloat(data)]

# if __name__ == '__main__':
#     import cv2
#     yolo = MyYolo()
#     img = cv2.imread("./test1.jpg")
#     data = yolo.plug(img)
