import os, time, platform
import LINE

LINE.login("TEST", "aaaa", "")   # 登入賴，程式自動發送登入驗證碼至手機信箱
while True:
    time.sleep(1)
#LINE.choose_room("110級機器人一甲")                            # 進賴群
#LINE.send("我是一條訊息")  
