import time
from datetime import timedelta

from flask import Flask
from flask import render_template
from flask import request, jsonify

from baiduAPI import BaiduAPI
from fireControl import FireControl
from mapHelper import Map
from radar import Radar

fc = FireControl(debug=False)
rd = Radar()
mp = Map()
bd = BaiduAPI()

web = Flask(__name__,
            template_folder='./html',
            static_folder='./static')
web.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=30)  # 设置过期时间


def timer(func):  # 记录计算时间
    def wrapped(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        with open("tmp.txt", "a") as f:
            f.write(str(t2 - t1) + "\n")
        return res

    return wrapped


# 设置返回html文件
@web.route("/")
def html_home():
    return render_template('index.html')


@web.route("/radar")
def html_radar():
    return render_template('radar.html')


@web.route("/radar/fitWindows")
def html_fitWindows():
    return render_template('fitWindows.html')


@web.route("/map")
def html_map():
    return render_template('map.html')


# 设置接口
@web.route("/compute")
# @timer
def api_compute():
    responseData = {"num": fc.compute()}
    # print("debug,response:",responseData)
    return jsonify(responseData)


@web.route("/getRadarInfo")
def api_getRadarShipInfo():
    img = rd.getImg()
    msg = bd.ocr(img)
    if (msg != 0):
        msg = rd.getRadarShipList(msg)
    else:
        msg = ["查询失败", 0]
    responseData = {
        "len": len(msg),
        "list": msg
    }
    return jsonify(responseData)


@web.route("/radar/fitWindows/fit")
def api_fitWindows():
    # 接收图片类型，增量，增量方向对捕获位置进行修改，然后返回修改后的图片
    imageType = int(request.args.get("type", 1))
    incr = int(request.args.get("incr", 0))
    toward = int(request.args.get("toward", 0))
    fc.sc.modify(imageType, incr, toward)
    image = fc.testImg(imageType)
    return image


@web.route("/getMapInfo")
def api_getMapInfo():
    image = mp.getImg()
    msg = bd.ocr(image)
    if (msg != 0):
        path, state = mp.getPath(msg)
    else:
        path, state = "", 0
    responseData = {
        "state": state,
        "path": path
    }
    return jsonify(responseData)


web.run(host="0.0.0.0", port=80, debug=False)
