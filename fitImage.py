import cv2


class ImageModifier():
    def __init__(self):
        self.size = (640, 640)

    def fit(self, url):
        img = cv2.imread(url)
        # 修改形状为640x640
        img = cv2.resize(img, self.size, interpolation=cv2.INTER_NEAREST)
        # 灰度处理
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img


if __name__ == '__main__':
    import os

    loadPath = r""
    savePath = r""
    # 获取所有图片
    dirList = os.listdir(loadPath)
    im = ImageModifier()
    for path in dirList:
        load = loadPath + path
        img = im.fit(load)
        # 保存
        cv2.imwrite(savePath + path, img)
    print("end")
