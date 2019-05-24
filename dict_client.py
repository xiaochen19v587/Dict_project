"""
  dict客户端部分
  发起请求,展示结果
"""
from socket import *
from getpass import getpass
import sys

# 全局变量
HOST = '176.234.8.10'
PORT = 8000
ADDR = (HOST, PORT)

# 所有函数都用s
s = socket()
s.connect(ADDR)


# 注册
def do_register():
    while 1:
        name = input('User:')
        pwd01 = getpass()
        pwd02 = getpass('Again:')
        if ' ' in name or ' ' in pwd01:
            print('用户名或密码不能有空格')
            continue
        if pwd01 != pwd02:
            print('两次密码不一致')
            continue
        msg = "R %s %s" % (name, pwd01)
        # 发送请求
        s.send(msg.encode())
        # 接收反馈
        data = s.recv(1024).decode()
        if data == 'OK':
            print('注册成功')
            login(name)
        else:
            print('注册失败')
        return


# 登录
def do_login():
    name = input('User:')
    pwd = getpass()
    msg = "L %s %s" % (name, pwd)
    # 发送请求
    s.send(msg.encode())
    # 接收反馈
    data = s.recv(1024).decode()
    if data == 'OK':
        print('登录成功')
        login(name)
    else:
        print('登录失败')
    return


# 查单词
def do_query(name):
    while 1:
        word = input('单词:')
        if word == '##':  # 结束单词查询
            break
        msg = 'Q %s %s' % (name, word)
        s.send(msg.encode())
        #  等待回复
        data = s.recv(4096).decode()
        print(data)


# 历史记录
def do_history(name):
    msg = 'H %s' % name
    s.send(msg.encode())
    # 等待回复
    data = s.recv(128).decode()
    if data == "OK":
        while 1:
            data = s.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print('没有历史记录.')

# 二级界面
def login(name):
    while 1:
        print("""
        ============Query============
        1.查单词   2.历史记录     3.注销
        =============================
        """)
        try:
            cmd = input('输入选项:')
            if cmd == '1':
                do_query(name)
            elif cmd == '2':
                do_history(name)
            elif cmd == '3':
                return
            else:
                print('请输入正确命令!')
        except KeyboardInterrupt:
            sys.exit('\n客户端退出.')


# 创建网络连接
def main():
    while 1:
        print("""
        ===========Welcome===========
        1.注册      2.登录       3.退出
        =============================
        """)
        try:
            cmd = input('输入选项:')
            if cmd == '1':
                do_register()
            elif cmd == '2':
                do_login()
            elif cmd == '3':
                s.send(b'E')
                break
            else:
                print('请输入正确命令!')
        except KeyboardInterrupt:
            sys.exit('\n客户端退出.')


if __name__ == '__main__':
    main()
