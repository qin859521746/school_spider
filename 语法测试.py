from school_spider import settings
import pymysql

class test():
    def __init__(self):
        self.host = settings.SQLSERVER_HOST
        self.db = settings.SQLSERVER_DBNAME
        self.user = settings.SQLSERVER_USER
        self.passwd = settings.SQLSERVER_PASSWD
        self.port = settings.SQLSERVER_PORT
    def process(self):
        # mysql=DBHelper(self.host,self.port,self.db,self.user,self.passwd)
        mysql=pymysql.connect(host=settings.SQLSERVER_HOST,user=settings.SQLSERVER_USER,password=settings.SQLSERVER_PASSWD,port=settings.SQLSERVER_PORT,db=settings.SQLSERVER_DBNAME,charset='utf8')
        cursor=mysql.cursor()
        # sql = "insert into easy(column_1,column_2) values (%s,%s)"
        create_school = '''CREATE TABLE IF NOT EXISTS school(
                              schoolName VARCHAR(100) NOT NULL,
                              schoolLocation VARCHAR(100) NOT NULL ,
                              schoolBeto VARCHAR(100) NOT  NULL ,
                              schoolType VARCHAR (100) NOT NULL ,
                              schoolLevel VARCHAR (100) NOT NULL ,
                              schoolSatis FLOAT NOT NULL
                )'''
        # 插入数据
        sql_insert = '''INSERT INTO school (schoolName, schoolLocation, schoolBeto, schoolType, schoolLevel,
                schoolSatis) VALUES (%s,%s,%s,%s,%s,%s)'''
        para = [('schoolName', 'schoolLocation', 'schoolBeto', 'schoolType', 'schoolLevel',2.3)]
        # value1 = [('101', '头号玩家')]
        # value2 = ('102', '马里奥')
        # cursor.execute(create_school)
        cursor.executemany(sql_insert,para)
        mysql.commit()

if __name__ == '__main__':
    test=test()
    test.process()