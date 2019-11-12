#!/usr/bin/python3

import socket
import json

import game_parser

HOST = "127.0.0.1"
DISPATCH_PORT = 62000


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


def stop_connection(sock):
    data = "stop"
    sock.sendall(data.encode())


def send_to_server(sock, player):
    data = player.toJson()
    sock.sendall(data.encode())
    data = sock.recv(2048).decode()

    if data == "stop":
        return None
    
    return data
