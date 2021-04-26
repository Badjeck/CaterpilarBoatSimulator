import pygame
from sprites import *
from config import *
import threading
import sys
from Network import *
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

allPlayers = {}

class Thread(threading.Thread):
    def __init__(self, p):
        threading.Thread.__init__(self)
        self.player = p
        # Connection au serveur
        self.network = Network('localhost', 5555)
        self.network.connect()
        self.message = {'username': 'ujjjjj', 'nb_player': 3}
        self.network.send(self.message)
        # Reception des premieres données
        self.data = self.network.recv(1024)
        self.player.pos = self.data['pos'] # Récupération de l'objet player
        self.player.rect.x = self.player.pos[0]
        self.player.rect.y = self.player.pos[1]
        self.data['pos'] = self.player.pos 
        self.network.send(self.data)

    def run(self):
        while g.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            try:
                self.player.pos = [self.player.rect.x,self.player.rect.y]
                self.data = self.network.recv(1024)
                print(self.data, '\n')
                
                for k, v in self.data['allPlayers'].items():
                    print(self.player)
                    v = [int(v[0]), int(v[1])]
                    if k not in allPlayers.keys():
                        allPlayers[k] = Friends(g, v[0], v[1])
                    elif allPlayers[k] != v:
                        allPlayers[k].pos = v
                    
                    
                self.data['pos'] = self.player.pos
                self.network.send(self.data)
            except Exception as e:
                print(e)
                self.quit()
                break

    
    def quit(self):
        print("Client arrêté. Connexion interrompue.")
        self.network.client.close()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial',32)
        self.running = True

    def createMap(self):
        plaine = []
        marrai = []
        forest = []
        f = open('map.txt', 'r')
        Lines = f.readlines()

        for x,line in enumerate(Lines):
            for y, el in enumerate(line.strip("\n")):
                el = int(el)
                if el == 0 :
                    #marrai
                    Block(self,x,y,MARRAI)
                    marrai.append((x,y))
                elif el == 1 or el == 2 :
                    #plaine
                    Block(self,x,y,PLAINE)
                    plaine.append((x,y))
                elif el == 3 :
                    #foret peu profonde
                    Block(self,x,y,FORET1)
                elif el == 4 :
                    #foret dense
                    Block(self,x,y,FORET2)
                    forest.append((x,y))
                elif el == 5 :
                    #foret profonde
                    Block(self,x,y,FORET3)
                    forest.append((x,y))
                elif el == 6 :
                    #foret / début montagne
                    Block(self,x,y,MONTAGNE1)
                elif el == 7 :
                    #montagne                    
                    Block(self,x,y,MONTAGNE2)
                elif el == 8 :
                    #grosse Motagne
                    Block(self,x,y,MONTAGNE3)
                elif el == 9 :
                    #Sommet
                    Block(self,x,y,SOMMET)
                else:
                    Block(self,x,y,(255,0,0))
        f.close()
        
        # create city
        for x in range(10):
            i = random.randint(0, len(plaine))
            City(self, plaine[i][0] , plaine[i][1])

        #create enemy camp
        for x in range(2):
            i = random.randint(0, len(marrai))
            EnemyCamp(self, marrai[i][0] , marrai[i][1])

        #create forest
        for x in range(20):
            i = random.randint(0, len(forest))
            Forest(self, forest[i][0] , forest[i][1])


    def new(self):
        #new game start
        self.playing = True
    
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.places = pygame.sprite.LayeredUpdates()

        self.createMap()
        self.Player = Player(self,1,2)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def game_over(self):
        pass

    def intro_screen(self):
        pass

    def main(self):
        #game loop

        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False
    

g = Game()
g.new()
while g.running:
    Thread(g.Player).start()
    g.main()
    g.game_over()

pygame.quit()
sys.exit()