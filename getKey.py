import win32api as wapi

'''
keyCheck函数返回从上次调用到这次调用间输入的按键
'''
keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789":
    keyList.append(char)


def keyCheck():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


if __name__ == "__main__":
    while True:
        print(keyCheck())
