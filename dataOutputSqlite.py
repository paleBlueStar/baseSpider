
import sqlite3
from baseSpy import config
class dataOutputSqlite(object):
    def __init__(self):
        #初始化 连接数据库 创建表
        self.datas = []
        self.cx = sqlite3.connect('MTime.db')
        self.create_table()

    def create_table(self,table_name=config.TAB_NAME):
        value = '''
        id integer primary key,
        MovieId integer,
        MovieTitle varchar(40) NOT NULL,
        RatingFinal real not null default 0.0,
        ROtherFinal real not null default 0.0,
        RPictureFinal real not null default 0.0,
        RDirectorFinal real not null default 0.0,
        RStoryFinal real not null default 0.0,
        UserCount integer not null default 0,
        AttitudeCount integer not null default 0,
        TotalBoxOffice varchar(20) not null,
        TodayBoxOffice varchar(20) not null,
        Rank integer not null default 0,
        ShowDays integer not null default 0,
        isRelease integer not null
        '''
        self.cx.execute('create table if not exists %s(%s)'%(table_name,value))

    def store_data(self,data):
        if data != None:
            self.datas.append(data)
            if len(self.datas) > config.MAX_DATA_NUM:
                self.output_db()
        return

    def output_db(self,table_name =config.TAB_NAME ):
        for data in self.datas:
            try:
                self.cx.execute('insert into %s(MovieId,MovieTitle,RatingFinal,ROtherFinal,RPictureFinal'
                                ',RDirectorFinal,RStoryFinal,UserCount,AttitudeCount,TotalBoxOffice,TodayBoxOffice'
                                'Rank,ShowDays,isRelease) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'%(table_name,data))
                self.datas.remove(data)
            except Exception as e:
                print(e,data)
                continue
        self.cx.commit()

    def output_end(self):
        #关闭数据库 注意还有没存储的数据要存储
        if len(self.datas) > 0:
            self.output_db()
        self.cx.close()