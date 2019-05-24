"""
  dict 服务端部分
  处理请求逻辑
"""
from socket import *
from multiprocessing import Process
import signal
from operation_db import *
import sys

# 全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)


# 处理注册
def do_register(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    pwd = tmp[2]
    if db.register(name, pwd):
        c.send(b"OK")
    else:
        c.send(B"NO")


# 处理登录
def do_login(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    pwd = tmp[2]
    if db.login(name, pwd):
        c.send(b"OK")
    else:
        c.send(B"NO")


#  查单词
def do_query(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    # 插入历史记录
    db.insert_history(name, word)

    # 查询单词
    mean = db.query(word)
    if not mean:
        c.send('没有找到该单词.'.encode())
    else:
        msg = "%s : %s" % (word, mean)
        c.send(msg.encode())


# 查询历史记录
def do_history(c, db, data):
    name = data.split(' ')[1]
    hist = db.history(name)
    if not hist:
        c.send('FAIL'.encode())
        return
    c.send(b"OK")
    for item in hist:
        msg = '%s   %s   %s' % item
        c.send(msg.encode())
        time.sleep(0.1)
    time.sleep(0.1)
    c.send(b"##")

# 处理客户端请求
def do_request(c, db):
    db.create_cursor()  # 生成游标 db.cur
    while 1:
        data = c.recv(1024).decode()
        if not data or data[0] == 'E':
            c.close()
            sys.exit('客户端退出.')
        elif data[0] == 'R':
            do_register(c, db, data)
        elif data[0] == 'L':
            do_login(c, db, data)
        elif data[0] == 'Q':
            do_query(c, db, data)
        elif data[0] == 'H':
            do_history(c, db, data)


# 网络连接
def main():
    # 创建数据库连接对象
    db = Database()

    # 创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 等待客户端连接
    print('Listen the port 8000...')
    while 1:
        try:
            c, addr = s.accept()
            print('Connect from', addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit('服务器退出.')
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        p = Process(target=do_request, args=(c, db))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
