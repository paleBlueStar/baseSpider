class urlManager(object):
    def __init__(self):
        self.newUrls = set()
        self.oldUrls = set()

    def has_new_url(self):
        # 判断是否有未爬取的url
        return self.newUrls_size() != 0

    def get_new_url(self):
        # 获取新的url
        new_url = self.newUrls.pop()
        self.oldUrls.add(new_url)
        return new_url

    def newUrls_size(self):
    # 获取未爬取的url数量
        return len(self.newUrls)

    def oldUrls_size(self):
    # 获取已爬取得url数量
        return len(self.oldUrls)

    def add_new_url(self,url):
        # 向url队列中添加新的url
        if url is None:
            return
        if url not in self.oldUrls and url not in self.newUrls:
            self.newUrls.add(url)

    def add_new_urls(self,urls):
        #x向队列中添加多个url
        if urls is None or len(urls) == 0:
            return
        else:
            for url in urls:
                self.add_new_url(url)
        # for i in range(len(urls)):
        #     if urls[i] is None:
        #         continue
        #     if urls[i] not in self.oldUrls and urls[i] not in self.newUrls:
        #         self.newUrls.add(urls[i])




