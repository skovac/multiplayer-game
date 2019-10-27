#!/usr/bin/python3

import socket

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


def make_laser_string(lasers):
    laserString = "$lasers<|"
    for laser in lasers:
        if laser.isShot:
            laserString += str(laser.x) + ":" + str(laser.y) + "|"
    laserString += ">"

    return laserString


def send_to_server(sock, playerID, x, y, lasers, oppInfo):
    data = "$id<" + str(playerID) + ">$x<" + str(x) + ">$y<" + str(y) + ">"
    data += make_laser_string(lasers)
    sock.sendall(data.encode())
    retString = sock.recv(1024).decode()
    oppInfo = game_parser.parse_info_string(retString, oppInfo)

    return oppInfo
