# -*- coding:utf-8 -*-
import socket, threading, re, select, urlparse3, pdb

lock = threading.Lock()
BUFFER = 8192


def HostPort(data):
    index = data.find('\n');
    firstLine = data[:index - 1];
    data = data[index + 1:];
    header = {};
    header['method'], header['url'], header['protocol'] = firstLine.split();
    host = urlparse3.urlparse(header['url'])[1];
    port = '80';
    if ':' in host:
        host, port = header['url'].split(':');
    port = int(port);
    ip = socket.gethostbyname(host);
    Request_data = '%s %s %s\r\n%s' % (header['method'], header['url'], header['protocol'], data)
    return (Request_data, ip, port);


def New_Link(sock, addr, index):
    while True:
        data = sock.recv(1024);
        lock.acquire();
        if (data):
            Request_info = HostPort(data);  # 把浏览器发来的请求处理了下,提取出来端口、并解析域名,修改请求头去除url留下请求的资源
            print(u'index: %d 请求信息如下:\n%s %s\n%s' % (index, Request_info[1], Request_info[2], Request_info[0]))
        else:
            break;
        lock.release();
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.connect(('127.0.0.1',8080));调试时候用
        s.connect((Request_info[1], Request_info[2]));
        s.send(Request_info[0]);
        while True:
            data = ''
            (rlist, wlist, elist) = select.select([s], [], [], 3)
            if rlist:
                data = rlist[0].recv(BUFFER)
                if len(data) > 0:
                    sock.send(data)
                else:
                    break;


class Client(object):
    def __init__(self):
        self.Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.Client_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 不知道放这里有没有意义
        self.Client_Socket.bind(('127.0.0.1', 6666));

    def Start(self):
        self.Client_Socket.listen(5);
        print('Start to listen 6666');
        index = 0;  # 用来标示启动了多少个线程
        while True:
            s, addr = self.Client_Socket.accept();
            index += 1;
            t = threading.Thread(target=New_Link, args=(s, addr, index));
            t.start();




if __name__ == '__main__':
    c = Client();
    c.Start();