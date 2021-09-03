# wows-helper
战舰世界辅助脚本
.  
│  baiduAPI.py：调用百度接口进行文字识别  
│  calculateAlpha.ipynb：计算出近距离下的炮击修正公式  
│  data.xlsx：存放记录测量到的近距离炮击数据  
│  fireControl.py：捕获屏幕，计算出标尺。同时还有捕获和保存图片，调用本地的ocr识别功能。  
│  fitImage.py：用于训练图片的预处理(已废用)  
│  getKey.py：捕获键盘输入，作为快捷键使用(已废用)  
│  getScreen.py：获取截图，测试捕获位置  
│  mapHelper.py：在读盘时查询当前地图的攻略信息  
│ requirements.txt：依赖环境  
│  radar.py：在读盘时查询雷达船的信息  
│  README.md  
│  setting.env：存放配置信息，需要手动填写百度云信息用于baiduAPI.py调用百度云接口  
│  setting1920x1080.json：1920x1080大小下的默认窗口信息  
│  web.py：启动flask服务  
├─.idea  
├─html：存放html模板  
├─img：存放yolo无法识别的图片  
├─machineLearning  
│  │  myYolo.py：调用yolo（已废用）  
│  │  MyYoloClass.py：调用yolo  
│  │  resetIndex.py：为训练图片和对应标签重新排序编号  
│  ├─models：yolo的接口文件  
│  ├─pt  
│  │  availableModel.pt：yolo模型文件  
│  ├─trainImg：训练数据  
│  │  ├─images  
│  │  └─labels  
│  ├─utils：yolo的接口文件  
│  ├─val：验证数据  
│  └─__pycache__  
├─static：存放html静态文件  
│  ├─css  
│  ├─img  
│  │  │  start.jpg  
│  │  └─map：用于存放地图攻略，可用自行添加地图。添加时只需将图片名改为地图名。  
│  └─js  
└─__pycache__  

### 需要修改的配置信息

配置信息文件是位于根目录的setting.env，只需将setting1920x1080.json中的数据复制进去并填写自己的百度云信息（用于）

启动服务后在前端界面中中测试捕获的窗口中是否清晰的显示了目标船速、落弹时间、距离和目标夹角。其中目标船速和目标夹角依赖于阿斯兰。

目标距离和船速图片要求清晰的数字，允许出现kn。落弹时间只允许出现数字。目标夹角需要清晰的数字，允许出现动画框。

### 配置环境

脚本的火控功能使用到yolo，需要英伟达显卡并安装cuda。
测试环境为windows，多次测量计平均值，GTX1650的计算速度为0.52秒，i5-9300h的计算速度为0.59秒。

配置越高的电脑计算速度越快。

使用pip install -r requirements.txt来安装所依赖的环境，如果有漏掉的包再手动安装即可。

这个脚本同时也依赖于战舰世界阿斯兰的插件

1. 显示目标最大航速6.1MB
2. 敌舰航线角，原版居中

### 已知bug

阿斯兰部分插件导致结算界面消失后，显示数值的位置会位移，需要重新定位。
