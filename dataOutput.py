#可以存为各种格式的文件，也可以存到数据库 改动空间很大
import codecs
from baseSpy import config
class dataOutput(object):
    def __init__(self):
        self.datas = []
    #此处写法有问题 数据量大的话会爆内存
    def store_data(self,data):
        # 解析出来的数据存到内存中
        if data is None:
            return
        # 改进 对插入的数据进行计数，超过限制则写入文件，同时清空内存
        if len(self.datas) < config.MAX_DATA_NUM:
            self.datas.append(data)
        else:
            self.outPut()

    def outPut(self):
        # fout = codecs.open('baike.htm','w',encoding='utf-8')
        #注意此处不是写入（w）而是添加（a） 因为是分批写入
        fout = codecs.open('baike.htm', 'a', encoding='utf-8')

        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>'%data['url'])
            fout.write('<td>%s</td>'%data['title'])
            fout.write('<td>%s</td>'%data['summary'])
            fout.write('</tr>')
            self.datas.remove(data)
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        #打开的文件记住要关闭###########
        fout.close()
        self.datas.clear()

    def output_end(self):
        if len(self.datas) > 0:
            self.outPut()
