import os
import pygame
import time
from datetime import datetime
import threading
import natsort
import random


def randomize_songs(files, target_length=None):
    print('here')
    if not files: return []
    if target_length is None: target_length = len(files)
    if len(files) < 2: return files
    first = random.choice(files)
    result = [first]
    while len(result) < target_length:
        previous = result[-1]
        possible_next_songs = files.copy()
        possible_next_songs.remove(previous)
        next_song = random.choice(possible_next_songs)
        result.append(next_song)

    previous = result[-2]
    possible_last_songs = files.copy()
    possible_last_songs.remove(previous)
    last_song = random.choice(possible_last_songs)
    result[-1] = last_song
    return result







def get_time_stamp():
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return time_str


def get_songs(folder_path, sorted=True, randomize=0):
    files = [file for file in os.listdir(folder_path) if file.endswith('.mp3')]
    if sorted:
        files = natsort.natsorted(files)
        return files
    if randomize > 0:
        length = max(randomize, len(files))
        files = randomize_songs(files, randomize)
        return files
    return None


class MP3Player:
    def __init__(self, folder_path, shuffle=True):
        self.verbose = True
        self.shuffle_songs = shuffle
        self.folder_path = folder_path
        self.mp3_files = get_songs(folder_path, sorted=True)
        self.current_index = -1
        self.events = []

        self.pause_auto_skip = False
        self.playing_paused = False
        self.stop_playing = False
        self.currently_playing = False
        self.last_message = ''

        if self.shuffle_songs: self.shuffle(reshuffle=False)

        pygame.init()
        pygame.mixer.init()

    def shuffle(self, reshuffle=True):
        songs = self.mp3_files.copy()
        last_song = songs[-1]
        if len(songs) < 2: return
        while True:
            random.shuffle(songs)
            if self.mp3_files[0] != last_song: break
        if not reshuffle: random.shuffle(songs) #in this case we don't want to set constraints
        self.mp3_files = songs
        self.append_event('Shuffled songs')

    def current_song(self):
        if self.current_index == -1: return "None"
        song = self.mp3_files[self.current_index]
        return song

    def append_event(self, event):
        time_stamp = get_time_stamp()
        current_song = self.current_song()
        entry = [time_stamp, event, current_song]
        self.last_message = time_stamp + ',' + event + ',' + current_song
        if self.verbose: print(entry)
        self.events.append(entry)

    def play_next(self):
        self.current_index += 1
        if self.current_index < len(self.mp3_files):
            mp3_file = os.path.join(self.folder_path, self.current_song())
            pygame.mixer.music.load(mp3_file)
            pygame.mixer.music.play()
            self.append_event("Playing new song")
            # Set up the MUSIC_END event here
            MUSIC_END = pygame.USEREVENT + 1
            pygame.mixer.music.set_endevent(MUSIC_END)

        else:
            self.current_index = -1
            self.append_event("End of playlist reached")
            if self.shuffle_songs: self.shuffle()
            self.play_next()

    def pause(self):
        if not self.playing_paused:
            pygame.mixer.music.pause()
            self.append_event("Song paused")
            self.playing_paused = True

    def resume(self):
        if self.playing_paused:
            pygame.mixer.music.unpause()
            self.append_event("Song resumed")
            self.playing_paused = False

    def skip(self):
        self.pause_auto_skip = True
        pygame.mixer.music.stop()
        self.append_event("Skipped to the next song")
        self.play_next()
        self.pause_auto_skip = False

    def handle_end_event(self, event):
        if event.type == (pygame.USEREVENT + 1):
            self.append_event("Current song ended.")
            if not self.pause_auto_skip: self.play_next()

    def thread_function(self):
        self.play_next()
        while True:
            if self.stop_playing:
                pygame.mixer.music.stop()
                self.append_event('Stopped playing')
                self.currently_playing = False
                self.current_index = -1
                return
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                else:
                    self.handle_end_event(event)

    def start(self):
        if self.currently_playing: return
        self.stop_playing = False
        thread = threading.Thread(target=self.thread_function)
        thread.start()
        self.currently_playing = True

    def stop(self):
        self.stop_playing = True
        MUSIC_END = pygame.USEREVENT + 2
        pygame.mixer.music.set_endevent(MUSIC_END)
