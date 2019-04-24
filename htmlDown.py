import requests
from baseSpy import config

class htmlDown(object):
    # def __init__(self,url):
    #     self.url = url

    def download(self,url):
        # 下载url队列中的网页
        if url is None:
            return
        s = requests.session()
        # s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) ' \
        #                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        # r = s.get(url,headers = config.HEADERS,timeout = config.TIMEOUT,encoding = config.ENCODEING)
        r = s.get(url,headers = config.HEADERS);r.encoding = config.ENCODEING
        if r.status_code == 200:
            return r.text
        print(r.status_code)
        return None

