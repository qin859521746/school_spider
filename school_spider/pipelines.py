# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from school_spider import settings
from school_spider.items import schoolItem, majorItem


class SchoolSpiderPipeline(object):
    def __init__(self):
        self.host = settings.SQLSERVER_HOST
        self.db = settings.SQLSERVER_DBNAME
        self.user = settings.SQLSERVER_USER
        self.password = settings.SQLSERVER_PASSWD
        self.port = settings.SQLSERVER_PORT
        self.connection = pymysql.connect(
            host=self.host, user=self.user, password=self.password,
            port=self.port, db=self.db, charset='utf8'
        )
        self.cursor = self.connection.cursor()
        if not self.cursor:
            raise (NameError, "连接数据库失败")

    def __del__(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
            print(self.cursor, '__del__ cursor closed')
        if self.connection:
            self.connection.close()
            self.connection = None

    def process_item(self, item, spider):
        if isinstance(item, schoolItem):
            self.school_mysql(item)
        elif isinstance(item, majorItem):
            self.major_mysql(item)
        return item

    def major_mysql(self, item):
        create_school = '''CREATE TABLE IF NOT EXISTS major(
                              majorName VARCHAR(100) NOT NULL,
                              majorID VARCHAR(100) NOT NULL

                )'''
        # 插入数据
        sql_insert = '''INSERT INTO major (majorName, majorID) VALUES (%s,%s)'''
        para = [(item['majorName'], item['majorID'])]
        try:
            # 执行sql
            self.cursor.execute(create_school)
            self.cursor.executemany(sql_insert, para)
            # 提交到数据库
            self.connection.commit()
        except:  # 发生错误时回滚
            self.connection.rollback()

    def school_mysql(self, item):
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
        para = [(
            item['schoolName'], item['schoolLocation'], item['schoolBeto'], item['schoolType'], item['schoolLevel'],
            item['schoolSatis'])]
        try:
            # 执行sql
            self.cursor.execute(create_school)
            self.cursor.executemany(sql_insert, para)
            # 提交到数据库
            self.connection.commit()
        except:  # 发生错误时回滚
            self.connection.rollback()
