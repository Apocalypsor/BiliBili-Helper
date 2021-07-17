import datetime
import sys

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def printT(s):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush()


def postData(url, data=None, headers=None, cookies=None, retry=5, timeout=10):
    retry_strategy = Retry(total=retry, backoff_factor=0.1)

    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    response = http.post(
        url, data=data, headers=headers, cookies=cookies, timeout=timeout
    )

    return response
