from sys import *
from os import *
from socket import *
import threading
import time
import csv
import io


def send(sock):
    while True:
        msg = str(input())
        sock.send(msg.encode('utf-8'))


def receive(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
        except Exception as e:
            print("유저 disconnect" + str(e))
            for i in range(0, len(ip)):
                if ip[i] == addr[0]:
                    print("ip: ", addr[0])
                    del ip[i]
            return
        else:
            print('받은 데이터: ', data)
            splitData = data.split()
            com = splitData[0]
            if com == 'auth':
                print("auth 실행")
                # ip, port번호 저장
                f = io.open('user.csv', 'r', encoding='utf-8')
                read = csv.reader(f)
                index = 0
                check = False
                # ip 체크
                for line in read:
                    print(line)
                    if line == []:
                        break
                    if line[1] == addr[0] and line[2] == splitData[1]:
                        check = True
                    index += 1
                if check == True:
                    sock.send(("auth" + " 로그인성공.").encode('utf-8'))
                else:
                    f = io.open('user.csv', 'a', encoding='utf-8')
                    wr = csv.writer(f)
                    wr.writerow([index//3, addr[0], splitData[1]])
                    f.close()
                    sock.send(("auth" + " 로그인성공.").encode('utf-8'))
                    print('auth 실행 완료')
            elif com == 'online_users':
                print('online_users 실행')
                try:
                    iplist = 'online_users '
                    for i in ip:
                        iplist = iplist + " " + i
                    print(iplist)
                    sock.send(iplist.encode('utf-8'))
                except Exception as e:
                    print("ip가 존재하지 않습니다." + str(e))
                    return False
            elif com == 'check':
                print("연결 되어 있습니다.")


port = 8081


while True:
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(5)

    print('%d번 포트로 접속 대기중...' % port)

    connectionSock, addr = serverSock.accept()

    ip = []
    ip.append(addr[0])
    print(ip)
    print(str(addr), '에서 접속되었습니다.')

    print('|접속중인 유저|')
    for i in ip:
        print(ip)

    receiver = threading.Thread(target=receive, args=(connectionSock,))

    receiver.start()

    time.sleep(1)
    pass
