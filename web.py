import json
from datetime import timedelta

from bson import ObjectId
from flask import Flask
from flask import render_template
from flask import request, make_response

from baiduAPI import BaiduAPI
from fireControl import FireControl
from mapHelper import Map
from radar import Radar

# import time

fc = FireControl(debug=False)
rd = Radar()
mp = Map()
bd = BaiduAPI()

web = Flask(__name__,
            template_folder='./html',
            static_folder='./static')
web.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=30)  # 设置过期时间


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# 服务器设置客户端可以跨域访问
from flask_cors import CORS


@web.after_request
def af_request(resp):
    resp = make_response(resp)  ##需要导入一些函数
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    resp.set_cookie("test", "123")
    return resp


CORS(web, supports_credentials=True)


# 跨域访问结束

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
def api_compute():
    with open("time.txt", "a") as f:
        # t1 = time.time()

        responseData = {"num": fc.compute()}

        # print("debug,response:",responseData)
        # t2 = time.time()
        # f.write(f"{(t2-t1)}\n")
    return json.dumps(responseData, cls=JSONEncoder)


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
    return json.dumps(responseData, cls=JSONEncoder)


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
    return json.dumps(responseData, cls=JSONEncoder)


web.run(debug=False)
