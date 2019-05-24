import re
import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     passwd='123456',
                     database='dict',
                     charset='utf8')

c = db.cursor()
n = 0
file_open = open('dict.txt')
sql = 'insert into world  values (%s,%s,%s)'
while 1:
    try:
        file = file_open.read().split('\n')
        get_world = file[n].split(' ')
        world = get_world[0]
        get_world.remove(world)
        mean = ' '.join([i for i in get_world if i])
        n += 1
        c.execute(sql, [n, world, mean])
    except Exception:
        print(Exception)
        break
db.commit()
c.close()
db.close()
