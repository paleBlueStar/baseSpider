from baseSpy.htmlParse import htmlParse
from baseSpy.htmlDown import htmlDown
from baseSpy.urlManager import urlManager
from baseSpy.dataOutput import dataOutput
from baseSpy import config
import time
import requests
from baseSpy.dataOutputSqlite import dataOutputSqlite
class spiderMan(object):
    def __init__(self):
        self.manager = urlManager()
        self.download = htmlDown()
        self.parser = htmlParse()
        self.storData = dataOutput()

    def crawl(self,baseUrl = config.BASE_URL):
        self.manager.add_new_url(baseUrl)
        while self.manager.has_new_url() and self.manager.oldUrls_size() < config.MAX_CRAWL_NUM:
            try:
                new_url = self.manager.get_new_url()

                html = self.download.download(new_url)

                new_urls,data = self.parser.parser(new_url,html)

                # self.storData(data)

                self.manager.add_new_urls(new_urls)

                self.storData.store_data(data)
                self.storData.output_end()
                print('已经抓取了%d 个链接！！！'% self.manager.oldUrls_size())
            except:
               print('crawl failed')
        self.storData.outPut()
    def crawl_json(self,root_url):
        content = self.download.download(root_url)
        urls = self.parser.parse_url(root_url,content)
        for url in urls:
            try:
                t = time.strftime('%Y%m%d%H%M%S3282',time.localtime())
                rank_url = 'http://service.library.mtime.com/Movie.api' \
                           '?Ajax_CallBack=true' \
                           '&Ajax_CallBackType=Mtime.Library.Services' \
                           '&Ajax_CallBackMethod=GetMovieOverviewRating' \
                           '&Ajax_CrossDomain=1' \
                           '&Ajax_RequsetUrl=%s' \
                           '&t=%s' \
                           '&Ajax_CallBackArgument0=%s'%(url[0],t,url[1])
                rank_content = self.download.download(rank_url)
                data = self.parser.parse_json(rank_url,rank_content)
                self.storData.store_data(data)
            except Exception as e:
                print('crawl fail')
        self.storData.output_end()
        print('crawl finish!!!')


if __name__ == '__main__':
    spider_man = spiderMan()
    spider_man.crawl()

