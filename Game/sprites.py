import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        #define size
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0   

        #define visual
        image_to_load = pygame.image.load('img/Boat.png')
        image_to_load = pygame.transform.scale(image_to_load,(32,32))
        self.image = pygame.Surface([self.width,self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load,(0,0))

        #define hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color):
            self.game = game
            self._layer = BLOCK_LAYER
            self.groups = self.game.all_sprites, self.game.blocks
            pygame.sprite.Sprite.__init__(self, self.groups)

            self.x = x * BLOCKSIZE
            self.y = y * BLOCKSIZE
            self.width = BLOCKSIZE
            self.height = BLOCKSIZE

            self.image = pygame.Surface([self.width,self.height])
            self.image.fill(color)

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y



class City(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
            self.game = game
            self._layer = BLOCK_LAYER
            self.groups = self.game.all_sprites, self.game.places
            pygame.sprite.Sprite.__init__(self, self.groups)

            self.x = x * BLOCKSIZE
            self.y = y * BLOCKSIZE
            self.width = TILESIZE
            self.height = TILESIZE

            image_to_load = pygame.image.load('img/City.png')
            image_to_load = pygame.transform.scale(image_to_load,(32,32))
            self.image = pygame.Surface([self.width,self.height])
            self.image.set_colorkey(BLACK)
            self.image.blit(image_to_load,(0,0))

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

class Forest(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
            self.game = game
            self._layer = BLOCK_LAYER
            self.groups = self.game.all_sprites, self.game.places
            pygame.sprite.Sprite.__init__(self, self.groups)

            self.x = x * BLOCKSIZE
            self.y = y * BLOCKSIZE
            self.width = TILESIZE
            self.height = TILESIZE

            image_to_load = pygame.image.load('img/forest.png')
            image_to_load = pygame.transform.scale(image_to_load,(32,32))
            self.image = pygame.Surface([self.width,self.height])
            self.image.set_colorkey(BLACK)
            self.image.blit(image_to_load,(0,0))

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

class EnemyCamp(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
            self.game = game
            self._layer = BLOCK_LAYER
            self.groups = self.game.all_sprites, self.game.places
            pygame.sprite.Sprite.__init__(self, self.groups)

            self.x = x * BLOCKSIZE
            self.y = y * BLOCKSIZE
            self.width = TILESIZE
            self.height = TILESIZE

            image_to_load = pygame.image.load('img/enemy.png')
            image_to_load = pygame.transform.scale(image_to_load,(32,32))
            self.image = pygame.Surface([self.width,self.height])
            self.image.set_colorkey(BLACK)
            self.image.blit(image_to_load,(0,0))

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            
class Friends(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        #define size
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0   

        #define visual
        image_to_load = pygame.image.load('img/Boat.png')
        image_to_load = pygame.transform.scale(image_to_load,(32,32))
        self.image = pygame.Surface([self.width,self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change