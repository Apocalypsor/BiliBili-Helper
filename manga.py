# -*- coding: utf-8 -*-

# 定时
'''
0 8 * * * manga.py
'''

import sys
import time

from utilCommon import printT, postData
from utilLogin import login
from utilSendNotify import send

msg = ""

# 登陆
login_status, b = login()
if not login_status:
    sys.exit()

headers = {
    "User-Agent": "Mozilla/5.0 BiliDroid/6.4.0 (bbcallen@gmail.com) os/android model/M1903F11I mobi_app/android build/6040500 channel/bili innerVer/6040500 osVer/9.0.0 network/2",
}

# 开始签到
printT("哔哩哔哩漫画开始签到")
msg = msg + "哔哩哔哩漫画签到状态: "

r = postData(
    "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn",
    data={"platform": "android"},
    headers=headers,
    cookies=b.get_cookies()
)

printT("响应: " + r.text)
if r.json()["code"] == 0:
    printT("签到成功.")
    msg = msg + "签到成功🐶\n"
if r.json()["code"] == "invalid_argument":
    printT("今日已签到.")
    msg = msg + "今日已签到⚠\n"

time.sleep(2)

printT("哔哩哔哩漫画获取签到信息")
msg = msg + "哔哩哔哩漫画签到信息: "
r = postData(
    "https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo",
    headers=headers,
    cookies=b.get_cookies()
)

printT("累计签到" + str(r.json()["data"]["day_count"]) + "天🐶")
msg = msg + "累计签到" + str(r.json()["data"]["day_count"]) + "天🐶\n"

send("哔哩哔哩小助手", msg)
