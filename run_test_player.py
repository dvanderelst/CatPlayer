from library import Player

folder = 'songs'
player = Player.MP3Player(folder)
files = player.mp3_files
for x in files: print(x)
player.start()



