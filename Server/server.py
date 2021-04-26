import socket
from _thread import *
import sys
import threading
import time
import pickle
from redisManager import RedisManager
import json
import requests
import pygame
import random

class ApiManager:
    def __init__(self):
        self.url = 'http://127.0.0.1:5000'

    def getUsers(self):
        res = dict()
        req = requests.get(self.url+'/users')
        if req.status_code == 200:
            res['data'] = json.loads(req.text)['data']
            res['success'] = True
        else:
            res['data'] = 'Erreur'
            res['success'] = False
        return res

    def getUser(self, username):
        res = dict()
        req = requests.get(self.url+'/user/'+username)
        if req.status_code == 200:
            res['success'] = True
            res['data'] = json.loads(req.text)['data']
        else:
            res['success'] = False
            res['data'] = 'Erreur'
        return res

    def addUser(self, username, posx, posy):
        res = dict()
        data = {'username' : username, 'posx': posx, "posy": posy}
        req = requests.post(self.url+'/user', data=data)
        if req.status_code == 200:
            res['success'] = True
            res['data'] = json.loads(req.text)['data']
        else:
            res['success'] = False
            res['data'] = 'Erreur'
        return res

    def updateUser(self, username, posx, posy):
        data = {'username' : username, 'posx': posx, "posy": posy}
        req = requests.put(self.url+'/user/'+username, data=data)

class Player:
    def __init__(self, id, username, pos):
        self.id = id
        self.username = username
        self.pos = pos

# Variable du serveur
allThreads = {}
allPlayers = {}
redisManager = RedisManager()
apiManager = ApiManager()

class ThreadClient(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.player = None
        self.conn = conn
        self.addr = addr
        self.name = self.getName()
        self.needAction = False
        
    # Recois des données 
    def recv(self, lenght):
        return pickle.loads(self.conn.recv(lenght))

    # Envoie de données
    def send(self, data):
        self.conn.send(pickle.dumps(data))

    # Quitte de thread et supprime les données des joueurs
    def quit(self):
        print("Client arrêté. Connexion interrompue.")
        del allPlayers[self.addr[1]]
        del allThreads[self.addr[1]]
        self.conn.close()

    # Fonction principale du thread
    def run(self):
        try:
            data = self.recv(64)
            # Verifie si le compte est en BDD
            account = self.checkAccount(data['username'])
            self.player = Player(account['id'], account['username'], [account['posX'], account['posY']])
            allPlayers[account['id']] = {'pos': self.player.pos}
            self.addPostion()
            while True:
                # Message envoyé au clien
                message = {
                    'pos': allPlayers[account['id']]['pos'],
                    'allPlayers': self.allExceptMe()
                }
                # Envoie les données de jeu au joueur
                self.send(message)
                # Reçois les données du joueur
                data = self.recv(200)
                self.player.pos = data['pos']
                self.addPostion()
                # Actualise les données du joueur avec celles du serveur
                allPlayers[account['id']] = data

                print(self.player.id, '=', self.getPosition())
                time.sleep(2)
            # #allPlayers[self.addr[1]] = Player(self.addr[1], data['username'])
            # while True:
            #     message = {'dataPlayer': allPlayers[self.addr[1]], 'allPlayers': allPlayers, 'needAction': self.needAction, 'actualPlayers': len(allPlayers)}
            #     self.send(message)
            #     if self.needAction:
            #         print(pickle.loads(self.recv()))
            #         self.needAction = False
            #     print('========', self.addr[1], len(allPlayers[self.addr[1]].hand.cards))
            #     time.sleep(3)

        except Exception as e:
            print(self.addr[1],"se deconnecte")
            del allPlayers[account['id']]
            apiManager.updateUser(self.player.username, self.player.pos[0], self.player.pos[1])
            self.quit()

    def checkAccount(self, username):
        global apiManager
        req = apiManager.getUser(username)
        if req['success']:
            return req['data']
        else:
            req = apiManager.addUser(username,random.randint(1, 501), random.randint(1, 501))
            return req['data']

    def addPostion(self):
        redisManager.send(self.player.id, f'{self.player.pos[0]}x{self.player.pos[1]}')
    
    def getPosition(self):
        return redisManager.get(self.player.id)

    def allExceptMe(self):
        global allPlayers
        res = {}
        for k, v in allPlayers.items():
            if k != self.player.id:
                res[k] = v['pos']
        return res

# Thread de jeu
class ThreadServer(threading.Thread):
    def run(self):
        global allPlayers, allThreads
        pass
        # while True:
        #     print(allPlayers)
        #     time.sleep(1)
                    

class Server():
    def __init__(self, ip, port):
        self.ip = str(ip)
        self.port = int(port)

    def send(self, conn, message):
        conn.send(str.encode(message))

    def received(self, conn):
        return conn.recv(2048).decode()

    def run_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(1)
        try:
            self.s.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))
        self.s.listen()
        print("Serveur démarré")

        # Lance la boucle de jeu côté serveur
        TS = ThreadServer()
        TS.start()
        # Accepte les connections des clients entrants
        while True:
            conn, addr = self.s.accept()
            print(addr, ' Vient de se connecter!')
            allThreads[addr[1]] = [conn, ThreadClient(conn, addr)]
            allThreads[addr[1]][1].start()

if __name__ == '__main__':
    monServeur = Server('88.137.179.12', 5555)
    monServeur.run_server()