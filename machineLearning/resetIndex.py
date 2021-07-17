import os

# 此文件用于整理文件名

imgurl = r"./trainImg/images"
txturl = r"./trainImg/labels"
namelist = os.listdir(imgurl)
count = 0
for f in namelist:
    count += 1
    oldName = f.split(".")[0]

    try:  # 防止名字相同
        os.rename(f"{imgurl}/{oldName}.jpg", f"{imgurl}/img{count}.jpg")
        os.rename(f"{txturl}/{oldName}.txt", f"{txturl}/img{count}.txt")
    except:
        os.rename(f"{imgurl}/{oldName}.jpg", f"{imgurl}/ximg{count}.jpg")
        os.rename(f"{txturl}/{oldName}.txt", f"{txturl}/ximg{count}.txt")

namelist = os.listdir(imgurl)
# 处理重名文件
for f in namelist:
    if 'x' in f:
        print(f)
        os.rename(f"{imgurl}/{f}", f"{imgurl}/{f[1:]}")
        os.rename(f"{txturl}/{f[:-3]}txt", f"{txturl}/{f[1:-3]}txt")
