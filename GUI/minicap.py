# -*- coding: utf-8 -*-
from Banner import Banner
from queue import Queue
import socket
import threading
#from itsdangerous import bytes_to_int

class Stream(object):
    __instance = None
    __mutex = threading.Lock()
    def __init__(self, ip="127.0.0.1", port=1313, queue=Queue()):
            self.IP = ip
            self.PORT = port
            self.banner = Banner()
            self.ReadImageStreamTask = None        
            self.picture = queue

    @staticmethod
    def getBuilder(ip, port, queue):
        """Return a single instance of TestBuilder object """
        if (Stream.__instance == None):
            Stream.__mutex.acquire()
            if (Stream.__instance == None):
                Stream.__instance = Stream(ip, port, queue)
            Stream.__mutex.release()
        return Stream.__instance

    def run(self):
        self.minicapSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #定义socket类型，网络通信，TCP
        self.minicapSocket.connect((self.IP,self.PORT))       
        self.ReadImageStreamTask = threading.Thread(target=self.ReadImageStream).start()
    
    
    def ReadImageStream(self):
        readBannerBytes = 0
        bannerLength = 2
        readFrameBytes = 0
        frameBodyLength = 0
        frameBody = b""
        while True:
            chunk = self.minicapSocket.recv(1024)
            chunk_len = len(chunk)
            if not chunk_len:
                continue
            cursor = 0
            while cursor < chunk_len:
                if readBannerBytes < bannerLength:
                    if readBannerBytes == 0:
                        self.banner.Version = chunk[cursor]
                    elif readBannerBytes == 1:
                        bannerLength = chunk[cursor]
                        print(bannerLength)
                        self.banner.Length = bannerLength
                    elif readBannerBytes in (2, 3, 4, 5):
                        self.banner.Pid += chunk[cursor] << (readBannerBytes - 2) * 8
                    elif readBannerBytes in (6, 7 ,8, 9):
                        self.banner.RealWidth += chunk[cursor] << (readBannerBytes - 6) * 8
                    elif readBannerBytes in (10, 11, 12, 13):
                        self.banner.RealHeight += chunk[cursor] <<  (readBannerBytes - 10) * 8
                    elif readBannerBytes in (14, 15, 16, 17):
                        self.banner.VirtualWidth += chunk[cursor] <<  (readBannerBytes - 14) * 8
                    elif readBannerBytes in (18, 19, 20, 21):
                        self.banner.VirtualHeight += chunk[cursor] <<  (readBannerBytes - 18) * 8
                    elif readBannerBytes == 22:
                        self.banner.Orientation += chunk[cursor]
                    elif readBannerBytes == 23:
                        self.banner.Quirks = chunk[cursor]
                    cursor += 1
                    readBannerBytes += 1
                    if readBannerBytes == bannerLength:
                        print(self.banner.toString())
                elif readFrameBytes < 4:
                    frameBodyLength += chunk[cursor] << readFrameBytes * 8
                    cursor += 1
                    readFrameBytes += 1
                else:
                    if chunk_len - cursor >= frameBodyLength:
                        frameBody += chunk[cursor:cursor + frameBodyLength]
                        cursor += frameBodyLength
                        self.picture.put(frameBody)
                        
                        frameBodyLength = readFrameBytes = 0
                        frameBody = b""
                        
                    else:
                        frameBody += chunk[cursor:chunk_len]
                        frameBodyLength -= chunk_len - cursor
                        readFrameBytes += chunk_len - cursor
                        cursor = chunk_len
                    


#     print a.picture