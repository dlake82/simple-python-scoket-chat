from socket import *
import threading
import time


def send(sock):
    while True:
        sendData = input('>>> ')
        if sendData == '>>> end':
            return
        sock.send(sendData.encode('utf-8'))


def receive(sock):
    while True:
        try:
            recvData = sock.recv(1024).decode('utf-8')
        except Exception as e:
            print("서버 접속 에러: " + str(e))
            return
        else:
            data = recvData.split()
            com = data[0]
            if com == 'auth':
                print(data[1])
            if com == 'online_users':
                print("online_users")
                temp = ''
                for i in range(1, len(data)):
                    temp = temp + " " + data[i]
                    print(temp)


def peerreceive(sock):
    while True:
        try:
            peerData = sock.recv(1024).decode('utf-8')
        except Exception as e:
            print("메세지 전송 에러: " + str(e))
            return
        else:
            print("상대방: ", peerData)


def login(sock):
    auth = ('auth ' + str(myport))
    print(auth)
    sock.send(auth.encode('utf-8'))


def _help():
    print("- help : lookup commands (display all possible commands)")
    print("- online_users: send a request to the regiServer, get back a list of all online peers and display them on the screen")
    print(
        "- connect [ip] [port] : request to chat with peer with the given IP and port")
    print("- disconnect [peer] : end your chat session with the listed peer")
    print("- talk [peer] [message] : send a message to the peer that you've already initiated a chat with via the connect command")
    print("- logoff : send a message (notification) to regiServer for logging off the chat system")


def msgsend(sock):
    while True:
        msg = str(input("메세지 입력: "))
        sock.send(msg.encode('utf-8'))
        print("메세지 전송")


def msgreceive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            print("상대방: ", msg)
        except:
            pass


def connect(sock):

    msgsender = threading.Thread(target=msgsend, args=(sock,))
    msgreceiver = threading.Thread(target=msgreceive, args=(sock,))

    msgsender.start()
    msgreceiver.start()


def listener(sock):
    while True:
        sock.listen(5)
        connectSock, addr = sock.accept()
        print(addr[0], " 와 연결되었습니다.\n")
        msgsender = threading.Thread(target=msgsend, args=(sock,))
        msgreceiver = threading.Thread(target=msgreceive, args=(sock,))

    msgsender.start()
    msgreceiver.start()


port = 8081
myport = 8083
clientSock = socket(AF_INET, SOCK_STREAM)

try:
    clientSock.connect(('127.0.0.1', port))
except Exception as e:

    print("연결 실패: " + str(e))

else:

    login(clientSock)
    pearSock = socket(AF_INET, SOCK_STREAM)
    pearSock.bind(('', myport))
    print('접속 완료')

    sender = threading.Thread(target=send, args=(clientSock, ))
    receiver = threading.Thread(target=receive, args=(clientSock, ))
    listener = threading.Thread(target=listener, args=(pearSock, ))

    listener.start()
    receiver.start()

    while True:

        time.sleep(1)

        command = str(input("메세지 입력: ")).split()
        com = command[0]
        if com == 'help':
            _help()
        elif com == 'online_users':
            print('online_users 실행')
            clientSock.send(('online_users').encode('utf-8'))
        elif com == 'connect':
            print('connect 실행')
            connectSock = socket(AF_INET, SOCK_STREAM)
            # 에러처리
            connectSock.connect((command[1], int(command[2])))
            connect(connectSock)
        elif com == 'check':
            print('check 실행')
            clientSock.send(('check').encode('utf-8'))
        else:
            pass
        time.sleep(1)
        pass
