import os
import socket
from tkinter.constants import FALSE, S, TRUE 
from threading import Thread
import requests
from time import time, sleep
import json
from tkinter import *
import tkinter
import tkinter as tk
from datetime import datetime

LARGE_FONT = ("verdana", 15,"bold")
now = datetime.now()
DATE = now.strftime("%y_%m_%d")
FORMAT = "utf8"

#======Chấp nhận kết nối ========
def accept_client():
    while True:
        conn, addr = s.accept()
        print("client address:",addr)
        try:
            Thread(target=handle_client, args=(conn,addr,)).start()   #tạo luồng cho các client, mỗi luồng một client chạy riêng
        except:
            print("Client", addr, "has been crashed accidentally!")
            conn.close()
            return

          

#======Nhận username & pass ======
def handle_client(conn, addr):
    try:
        username = conn.recv(1024).decode(FORMAT)
        if username == "quit":
                print("User quit")
                conn.close()
        password = conn.recv(1024).decode(FORMAT)
        choose = conn.recv(1024).decode(FORMAT)

        #check username và password
        checkLogin(conn,choose,username,password)
        
        #=====Nếu người dùng nhập chữ "quit" vào ô "Date" thì sẽ thoát chương trình
        def receive_stop():
            receive = input()
            if input == 'quit':
                conn.send(receive.encode(FORMAT))
        stop_thread = Thread(target = receive_stop)
        stop_thread.start()
        while True:
            msg = conn.recv(1024).decode(FORMAT)
            if msg == "quit":
                print("User", username, "quit")
                conn.close()
                break
            else: 
                #xử lí dữ liệu ở đây
                msg2 = conn.recv(1024).decode(FORMAT)
                print("User", username, "search", msg, msg2)
                if msg >= DATE:
                    getDataFromWeb(DATE)
                sendInformationToClient(msg,msg2,conn)
    
    except:
        print("Client", addr, "has been crashed accidentally!")
        return
    
#====Hàm lấy dữ liệu từ third party và lưu vào file dạng json=======
def getDataFromWeb(date):
    response = requests.get("https://coronavirus-19-api.herokuapp.com/countries")
    data = response.json()
    jsonObject = json.dumps(data, indent = 12)
    filenamejson = date
    with open(filenamejson+".json", "w") as fout:
        fout.write(jsonObject)

#====Hàm gửi dữ liệu Covid dựa theo ngày/tháng/năm và quốc gia mà Client nhập====
def sendInformationToClient(date,request,client):
    with open(date+".json", "r") as fin:
        data = json.load(fin)
    for i in data: 
        if i["country"] == request:
            sendInfor = "Country: " + str(i["country"]) + "\nCase: " + str(i["cases"]) + "\nTodayCases: " + str(i["todayCases"]) + "\nDeath: " + str(i["deaths"]) + "\nToday Death: " + str(i["todayDeaths"]) + "\nRecovered: " + str(i["recovered"]) + "\nActive: " + str(i["active"]) + "\nCritical: " + str(i["critical"]) + "\nCase per one millions: " + str(i["casesPerOneMillion"]) + "\nDeath per onr millions: " + str(i["deathsPerOneMillion"]) + "\nTotal test: " + str(i["totalTests"]) + "\nTest per one million: " + str(i["testsPerOneMillion"])
            client.sendall(bytes(sendInfor, "utf8"))
        fin.close()

#=====Hàm kiểm tra đăng nhập/đăng ký =======
def checkLogin(conn,choose,username, password):
    file = open("user.txt", "a+")      
    file.seek(0)
    if choose == "1":
        tmp = TRUE
        lines = file.readlines()
        for line in lines:
            usFile = line.strip("\n").split(",")
            if username == usFile[0] and password == usFile[1]:
                message = "Sign in successfully"
                print(username, message)
                conn.send(message.encode(FORMAT)) 
                tmp = FALSE
                break
        if tmp == TRUE:
            message = "Unregistered"
            print(username, message)
            conn.send(message.encode(FORMAT)) 

    elif choose == "2":
        tmp = TRUE
        lines = file.readlines()
        for line in lines:
            usFile = line.strip("\n").split(",")
            if username == usFile[0]:
                message = "Account has been registered"
                print(username, message)
                conn.sendall(bytes(message, FORMAT))
                tmp = FALSE
        if tmp == TRUE:
            file.write('\n')
            file.write(username + "," + password )
            message = "Sign up successfully!"
            print(username, message)
            conn.sendall(bytes(message, FORMAT)) 
    file.close()

#=====Khai báo HOST và PORT cho server=====
HOST = "127.0.0.1" 
SERVER_PORT = 65432       

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((HOST, SERVER_PORT))

#Hàm main
if __name__ == "__main__":
    s.listen(5)
    print("SERVER SIDE")
    print("server:", HOST, SERVER_PORT)
    print("Chờ kết nối từ các client...")
    ACCEPT_THREAD = Thread(target = accept_client)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    s.close()

