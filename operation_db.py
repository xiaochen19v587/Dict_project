"""
  dict项目用于处理数据
"""
import pymysql
import hashlib
import time


# 编写功能类  提供给服务端使用
class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 passwd='123456',
                 database='dict',
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()  # 连接数据库

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.cur.close()
        self.db.close()

    # 处理注册
    def register(self, name, pwd):
        sql = 'select * from user_info where name="%s"' % name
        self.cur.execute(sql)
        r = self.cur.fetchone()  # 如果查询到结果
        if r:
            return False

        # 生成加密对象,参数为盐
        hash = hashlib.md5((name + 'wmh').encode())
        # 对密码进行算法加密
        hash.update(pwd.encode())
        # 获取加密后的密码字串
        # hash.hexdigest()

        sql = 'insert into user_info (name,passwd) values (%s,%s)'
        try:
            self.cur.execute(sql, [name, hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self, name, pwd):
        hash = hashlib.md5((name + 'wmh').encode())
        hash.update(pwd.encode())
        sql = 'select * from user_info where name=%s and passwd=%s'
        r = self.cur.execute(sql, [name, hash.hexdigest()])
        if r:
            return True
        else:
            return False

    def insert_history(self, name, word):
        sql = 'insert into hist (name,word,time) values (%s,%s,%s)'
        self.cur.execute(sql, [name, word, time.ctime()])
        self.db.commit()

    def query(self, word):
        sql = 'select mean from world where world=%s'
        self.cur.execute(sql, word)
        r = self.cur.fetchone()
        if r:
            return r[0]

    def history(self, name):
        sql = 'select name,word,time from hist where name=%s order by id desc limit 10'
        self.cur.execute(sql, [name])
        r = self.cur.fetchmany(10)
        if r:
            return r
