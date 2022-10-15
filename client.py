import socket
from tkinter import *
from threading import Thread
import tkinter
import tkinter as tk
import requests
import opcode
import time
import json
from tkinter import messagebox
from datetime import datetime

now = datetime.now()
DATE = now.strftime("%y_%m_%d")
LARGE_FONT = ("verdana", 13,"bold")

#=====Bấm Sign in button thì hàm này chạy=====
def client_login(event=None):
    submittedUsername = username.get()
    submittedPassword = password.get()
    if submittedUsername == "" or submittedPassword == "": 
        messagebox.showinfo('Message ','Empty. Please try again :) ')
        on_closing()
    else:
        client.send(submittedUsername.encode(FORMAT))
        time.sleep(0.01)
        client.send(submittedPassword.encode(FORMAT))
        time.sleep(0.01)
        client.send("1".encode(FORMAT))
        msg = client.recv(1024).decode(FORMAT)
        if msg == "Sign in successfully":
            messagebox.showinfo('Message',msg)
            homepage()
        else: 
            messagebox.showinfo('Message ','Sign in failed. Please try again :) ')
            on_closing()

#=====Bấm Sign up button thì hàm này chạy=====
def client_logup(event=None):
    submittedUsername = username.get()
    submittedPassword = password.get()
    if submittedUsername == "" or submittedPassword == "": 
        on_closing()
    else:
        client.send(submittedUsername.encode(FORMAT))
        time.sleep(0.01)
        client.send(submittedPassword.encode(FORMAT))
        time.sleep(0.01)
        client.send("2".encode(FORMAT))
        msg = client.recv(1024).decode(FORMAT)
        if msg == "Sign up successfully!":
            messagebox.showinfo('Sign up successfully!','Your username: '+submittedUsername + '  & Your pass: ' + submittedPassword)
            homepage()
        elif msg == 'Account has been registered':
            messagebox.showinfo('Message ','Account has been registered. Please try again :) ')
            on_closing()

#==========GUI HOMEPAGE========
def homepage():

    top.destroy() #xóa cái box loggin
    top2 =Tk() #tạo box mới (homepage)
    top2.title("Homepage")
    top2.geometry("500x400")
    top2.configure(bg="bisque2")
    label_title = tk.Label(top2, text="HOME", font=LARGE_FONT,fg='#20639b',bg="bisque2")
    label_wel = tk.Label(top2, text="Welcome to Coronavirus (COVID-19) Dashboard",fg='#20639b',bg="bisque2",font='verdana 10 ')
    key_search =tkinter.StringVar()
    key_search2 =tkinter.StringVar()
    key_search.set(DATE)
    key_search2.set("World")
    entry_search = tk.Entry(top2,width=37,bg='light yellow', textvariable= key_search)
    entry_search2 = tk.Entry(top2,width=37,bg='light yellow', textvariable= key_search2)

    #=====Bấm Button SEARCH thì hàm này chạy=====
    def search():
        key = key_search.get()
        key2 = key_search2.get()
        client.send(key.encode(FORMAT))
        client.send(key2.encode(FORMAT))
        key_search.set("")
        key_search2.set("")
        if key == "quit" or key2 == "quit":
            client.close()
            top2.destroy()
    
    #========Luồng Receive=======
    def receive():
        while True:
            try:
                msg = client.recv(4080).decode(FORMAT)
                if msg == 'quit':
                    messagebox.showinfo('Message ','Sever has stopped ')
                    client.close()
                    top2.destroy()
                # msg2 = client.recv(1024).decode(FORMAT)
                # msg3 = client.recv(1024).decode(FORMAT)
                # msg4 = client.recv(1024).decode(FORMAT)
                # msg5 = client.recv(1024).decode(FORMAT)
                # msg6 = client.recv(1024).decode(FORMAT)
                # msg7 = client.recv(1024).decode(FORMAT)
                # msg8 = client.recv(1024).decode(FORMAT)
                # msg9 = client.recv(1024).decode(FORMAT)
                # msg10 = client.recv(1024).decode(FORMAT)
                # msg11 = client.recv(1024).decode(FORMAT)
                # msg12 = client.recv(1024).decode(FORMAT)
                line = "-----------------------------"
                mess = msg.split("\n")
                msg_list.insert(tkinter.END, mess[0])
                msg_list.insert(tkinter.END, mess[1])
                msg_list.insert(tkinter.END, mess[2])
                msg_list.insert(tkinter.END, mess[3])
                msg_list.insert(tkinter.END, mess[4])
                msg_list.insert(tkinter.END, mess[5])
                msg_list.insert(tkinter.END, mess[6])
                msg_list.insert(tkinter.END, mess[7])
                msg_list.insert(tkinter.END, mess[8])
                msg_list.insert(tkinter.END, mess[9])
                msg_list.insert(tkinter.END, mess[10])
                msg_list.insert(tkinter.END, mess[11])
                msg_list.insert(tkinter.END, line)
            except OSError: 
                break
    
    receive_thread = Thread(target=receive)
    receive_thread.start()

    button_search = tk.Button(top2,text="SEARCH",bg="#20639b",fg='floral white', height=2)
    button_search['command'] = search
    msg_list = tkinter.Listbox(top2, height=16, width=74)

    label_title.pack()
    label_wel.pack()
    Label(top2, text = "Date (yy_mm_dd):",fg='#20639b',bg="bisque2",font='verdana 10 ').place(x = 20, y = 60)
    Label(top2, text = "Country",fg='#20639b',bg="bisque2",font='verdana 10 ').place(x = 20, y = 90)    
    entry_search.place(x = 150, y = 60)
    entry_search2.place(x = 150, y = 90)
    button_search.place(x=410, y = 61)
    msg_list.place(x = 20, y= 120 )
    def on_closing2():
        client.send("quit".encode(FORMAT))
        client.close()
        top2.destroy()
    top2.protocol("WM_DELETE_WINDOW", on_closing2)
    top2.mainloop()
        

#========Khi người dùng nhấn nút [X] thì đóng cửa sổ ngắt kết nối đến server===========
def on_closing():
    client.send("quit".encode(FORMAT))
    client.close()
    top.destroy()


#=========GUI LOGIN============
top = Tk()
top.title("Client")
top.geometry("300x200")
top.configure(bg="bisque2")

Label(top, text = "Username",fg='#20639b',bg="bisque2",font='verdana 10 ').place(x = 30, y = 40)
Label(top, text = "Password",fg='#20639b',bg="bisque2",font='verdana 10 ').place(x = 30, y = 80)
username = tkinter.StringVar()
password = tkinter.StringVar()
e1 = Entry(top, width = 25, textvariable = username).place(x = 120, y = 40)
e2 = Entry(top, width = 25, textvariable = password, show= '*').place(x = 120, y = 80)

button_login = Button (top,text="Sign in",bg="#20639b",fg='floral white',height= "1",width="15", activeforeground = "black", activebackground = "blue", command= client_login)
button_login.place(x=100,y=120)
button_logup = Button (top,text="Sign up",bg="#20639b",fg='floral white',height= "1",width="15", activeforeground = "black", activebackground = "blue", command= client_logup)
button_logup.place(x=100, y=160)

top.protocol("WM_DELETE_WINDOW", on_closing)

#================================

#hostip = input('Please input IP address: ')
HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect( (HOST, SERVER_PORT) )
top.mainloop()
