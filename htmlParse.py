#此部分因项目事宜 改动较大 parser 函数解析百度百科  parser_url解析时光网电影信息
# 网页解析器

from baseSpy import config
from bs4 import BeautifulSoup
import re
import urllib
import json
class htmlParse(object):
    def parser(self,page_url,html_const):
        # 对外接口
        soup = BeautifulSoup(html_const,config.PARSER,from_encoding=config.ENCODEING)
        new_urls = self._get_new_url(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data
        pass

    def _get_new_url(self,page_url,soup):
        #内部接口 负责解析新的url
        new_urls = set()
        links = soup.find_all('a',href=re.compile(r'^/item/.*$'))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls
        pass

    def _get_new_data(self,page_url,soup):
        data = {}
        data['url'] = page_url
        title = soup.find('dd',class_ = 'lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div',class_= 'lemma-summary')
        data['summary'] = summary.get_text()
        return data
        #内部接口 负责抽取新的数据
        pass
    def parse_url(self,page_url,response):
        pattern = re.compile(r'http://movie.mtime.com/(\d+)/')
        urls = pattern.findall(response)
        if urls != None:
            return list(set(urls))
        return None

    def parse_json(self,page_url,response):
        pattern = re.compile(r':(.*?);')
        result = pattern.findall(response)[0]
        if result != None:
            value = json.load(result)
            try:
                isRelease = value.get('value').get('isRelease')
            except Exception as  e:
                print(e)
                return None
        if isRelease:
            if value.get('value').get('hotValue') == None:
                return self._parse_release(page_url,value)
            else:
                return self._parse_not_release(page_url,value,isRelease = 2)
        else:
            return self._parse_not_release(page_url,value)

    def _parse_release(self,page_url,value):
        try:
            isRelease = 1
            value1 = value.get('value')
            movieRate = value1.get('movieRating')
            boxOffice = value1.get('boxOffice')
            movieTitle = value1.get('movieTitle')

            RPictureFinal = movieRate.get('RPictureFinal')
            RStoryFinal = movieRate.get('RStoryFinal')
            RDirectFinal = movieRate.get('RDirectorFinal')
            ROtherFinal = movieRate.get('ROtherFinal')
            RatingFinal = movieRate.get('RatingFinal')

            MovieId = movieRate.get('MovieId')
            UserCount = movieRate.get('UserCount')
            AttitudeCount = movieRate.get('AttitudeCount')

            TotalBoxOffice = boxOffice.get('TotalBoxOffice')
            TotalBoxOfficeUnit = boxOffice.get('TotalBoxOfficeUnit')
            TodayBoxOffice = boxOffice.get('TodayBoxOffice')
            TodayBoxOfficeUnit = boxOffice.get('TodayBoxOfficeUnit')

            ShowDays = boxOffice.get('ShowDays')


            try:
                rank = boxOffice.get('Rank')
            except Exception as e:
                # print(e)
                rank = 0
            return(MovieId,movieTitle,RatingFinal,ROtherFinal,RPictureFinal,RDirectFinal,
                   RStoryFinal,UserCount,AttitudeCount,TotalBoxOffice+TotalBoxOfficeUnit,
                   TodayBoxOffice+TodayBoxOfficeUnit,rank,ShowDays,isRelease)
        except Exception as e:
            print(e,page_url,value)




        # pass
    def _parse_not_release(self,page_url,value,isRelease=0):
        try:
            movieRate = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')

            RPictureFinal = movieRate.get('RPictureFinal')
            RStoryFinal = movieRate.get('RStoryFinal')
            RDirectFinal = movieRate.get('RDirectorFinal')
            ROtherFinal = movieRate.get('ROtherFinal')
            RatingFinal = movieRate.get('RatingFinal')

            MovieId = movieRate.get('MovieId')
            UserCount = movieRate.get('UserCount')
            AttitudeCount = movieRate.get('AttitudeCount')
            try:
                rank = value.get('hotValue').get('Rank')
            except Exception as e:
                rank = 0
            return (MovieId,movieTitle,RatingFinal,ROtherFinal,RPictureFinal,RDirectFinal,
                   RStoryFinal,UserCount,AttitudeCount,u'无',
                   u'无',rank,0,isRelease)
        except Exception as e:
            print(e,page_url,value)
            return None
        pass


