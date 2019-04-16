#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from itertools import zip_longest
from _thread import start_new_thread
import socket

HOST = ''
PORT = 1336
SLEEP_TIME = 0.5
PASSWORD = "12ab"


def compare_flag(password1, password2):
    
    if(len(password1) == 0):
        return False
    for left, right in zip_longest(password1, password2):
        if(left != right):
            return False
        sleep(SLEEP_TIME)  
    return True


def listen(host, port):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    print("Listenning ..")
    return s


def client_handle(conn):
    
    conn.send("\nEnter password: ".encode('utf-8'))
    data = ""
    while True:
    	data += conn.recv(1024).decode('utf-8')
    	if '\n' in data:
            data = data.splitlines()[0]
            break
    password = data
    if compare_flag(password, PASSWORD):
        conn.send("Right Password\n".encode('utf-8'))
    else:
        conn.send("Wrong Password\n".encode('utf-8'))
    conn.close()

if __name__ == "__main__":
   
    s = listen(HOST, PORT)
    while True:
    	conn, addr = s.accept()
    	start_new_thread(client_handle, (conn,))
    s.close()
