#!/usr/bin/python3

import socket
import json
import os

with open("cfg/config.json", "r") as cfgFile:
    serverData = json.load(cfgFile)
    HOST = serverData["server"]["host"]
    DISPATCH_PORT = int(serverData["server"]["port"])


def get_socket(playerID):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, DISPATCH_PORT))
    except:
        return None

    sock.sendall(playerID.encode())
    if "ok" in sock.recv(1024).decode():
        return sock

    return None


def stop_connection(sock, player):
    data = "stop"
    sock.sendall(data.encode())
    player.disconnected = True


def send_to_server(sock, player):
    if player.disconnected:
        return None

    data = player.toJson()
    sock.sendall(data.encode())
    data = sock.recv(2048).decode()

    if data == "stop":
        player.disconnected = True
        return None
    
    return data
