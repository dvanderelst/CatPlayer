from library import Player
import pygame
import time

folder = 'songs'
player = Player.MP3Player(folder)
print(player.mp3_files)
player.start()
