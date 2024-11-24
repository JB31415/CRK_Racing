import io
import os
import socket
import struct
import time
import picamera2
import sys,getopt
import functools



import asyncio 
from websockets.asyncio.server import serve
import websockets 

import threading
from collections import deque


from Thread import *
from threading import Thread
from Testing import Server
from server_ui import Ui_server_ui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#New

class mywindow(QMainWindow,Ui_server_ui):
    
    def __init__(self):
        self.user_ui=False
        self.start_tcp=True
        self.port = 8000
        self.parseOpt()

        self.TCP_Server=Server()

        if self.user_ui:
            self.app = QApplication(sys.argv)
            super(mywindow,self).__init__()
            self.setupUi(self)
            self.m_DragPosition=self.pos()
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setMouseTracking(True)
            self.Button_Server.setText("On")
            self.on_pushButton()
            self.Button_Server.clicked.connect(self.on_pushButton)
            self.pushButton_Close.clicked.connect(self.close)
            self.pushButton_Min.clicked.connect(self.windowMinimumed)
        
        if self.start_tcp:
            self.TCP_Server.StartTcpServer()
            self.ReadData=Thread(target=self.TCP_Server.readdata)
            self.SendVideo=Thread(target=self.TCP_Server.sendvideo)
            self.power=Thread(target=self.TCP_Server.Power)
            self.SendVideo.start()
            self.ReadData.start()
            self.power.start()
            if self.user_ui:
                self.label.setText("Server On")
                self.Button_Server.setText("Off")
                
    def getHasMessage(self):
        return self.TCP_Server.getHasMessage()
    
    def setHasMessage(self, message):
        self.TCP_Server.setHasMessage(message)
                
    def windowMinimumed(self):
        self.showMinimized()
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()
 
    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()
 
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False
        
    def parseOpt(self):
        self.opts,self.args = getopt.getopt(sys.argv[1:],"tnp")
        for o,a in self.opts:
            if o in ('-t'):
                print ("Open TCP")
                self.start_tcp=True
            elif o in ('-n'):
                self.user_ui=False
            elif o in ('-p'):
                self.port = 5001
                        
    def close(self):
        try:
           stop_thread(self.SendVideo)
           stop_thread(self.ReadData)
           stop_thread(self.power)
        except:
            pass
        try:
            self.TCP_Server.server_socket.shutdown(2)
            self.TCP_Server.server_socket1.shutdown(2)
            self.TCP_Server.StopTcpServer()
        except:
            pass
        print ("Close TCP")
        if self.user_ui:
            QCoreApplication.instance().quit()
        os._exit(0)
    def on_pushButton(self):
        if self.label.text()=="Server Off":
            self.label.setText("Server On")
            self.Button_Server.setText("Off")
            self.TCP_Server.tcp_Flag = True
            print ("Open TCP")
            self.TCP_Server.StartTcpServer()
            self.SendVideo=Thread(target=self.TCP_Server.sendvideo)
            self.ReadData=Thread(target=self.TCP_Server.readdata)
            self.power=Thread(target=self.TCP_Server.Power)
            self.SendVideo.start()
            self.ReadData.start()
            self.power.start()
            
        elif self.label.text()=='Server On':
            self.label.setText("Server Off")
            self.Button_Server.setText("On")
            self.TCP_Server.tcp_Flag = False
            try:
                stop_thread(self.ReadData)
                stop_thread(self.power)
                stop_thread(self.SendVideo)
            except:
                pass
            self.TCP_Server.StopTcpServer()
            print ("Close TCP")
            
    def spinOut(self):
        print("spin out")
        self.TCP_Server.spinOut()
    
#Global Variables



async def hello(websocket):
    
    print("Running Handler")
    myshow = mywindow()
    try:
        print(myshow.getHasMessage())
        
        if myshow.user_ui==True:
            myshow.show()
            myshow.app.exec_()
            
            #sys.exit(myshow.app.exec_())
        else:
            try:
                pass
            except KeyboardInterrupt:
                myshow.close()
        print("A")
       
   
    except KeyboardInterrupt:
        print("Exception called")
        myshow.close()
    
    
     #Repeat infinity
    while True: 
           
        #Set response to null
        response = "null"
            
        #If it has a message to send
        if(myshow.getHasMessage() == True):
            #Send message and set hasMessage to false
            await websocket.send("00")
            myshow.sethasMessage(False)
                
            #Else...
        else:
            try:
                   
                #Has to put things in front of this or else it gets timeout error
                #Look for response
                print(response)
                print("A")
                response =  await asyncio.wait_for(websocket.recv(), timeout=.25)
                    
                    
                    
                #If it times out, sleep to let other programs take over
            except(asyncio.TimeoutError):
                #print("A")
                await asyncio.sleep(0)
                
            #If recieve anything other than greeting as message, spinout
            if(response != "null"):
                myshow.spinOut()
                    
        
        
        #By awaiting for something at the end, it yields control back to the event handler. Prevents it from getting stuck essentially
        await asyncio.sleep(0)
    
    


async def main():
   async with serve(hello, "0.0.0.0", 8765):
            await asyncio.get_running_loop().create_future()  # run forever
    

if __name__ == '__main__':
    asyncio.run(main())
        
    
       
    
  

    
