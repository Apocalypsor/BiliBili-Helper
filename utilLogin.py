import json
import os

import utilBilibili as bilibili
from utilCommon import printT


def loadCookie():
    try:
        with open("bilibili_cookie.json", "r") as b:
            cookies = json.load(b)

        return True, cookies
    except json.decoder.JSONDecodeError:
        return False, "Failed to decode the json file!"
    except Exception as e:
        return False, f"Error, {e}"


def login():
    bili = bilibili.Bilibili()

    printT("尝试使用 Cookie 登陆")
    if os.path.isfile("bilibili_cookie.json"):
        load_status, cookies = loadCookie()
        if load_status:
            login_status = bili.login(**cookies)
            if login_status:
                printT("账号登陆成功")
                return True, bili

    printT("尝试使用密码登陆")
    username = os.environ["BILIBILI_USERNAME"]
    password = os.environ["BILIBILI_PASSWORD"]
    login_status = bili.login(username=username, password=password)
    if not login_status:
        printT("账号登陆失败")
        return False, None
    else:
        printT("账号登陆成功，保存 Cookies")
        cookies = bili.get_cookies()
        with open("bilibili_cookie.json", "w") as b:
            b.write(json.dumps(cookies, ensure_ascii=False, indent=4))

        return True, bili
