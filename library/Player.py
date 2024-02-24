import os
import pygame
import time
from datetime import datetime
import threading

def get_time_stamp():
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return time_str


def get_songs(folder_path):
    files = [file for file in os.listdir(folder_path) if file.endswith('.mp3')]
    return files


class MP3Player:
    def __init__(self, folder_path):
        self.verbose = True
        self.folder_path = folder_path
        self.mp3_files = get_songs(folder_path)
        self.current_index = -1
        self.events = []

        self.pause_auto_skip = False
        self.playing_paused = False
        self.stop_playing = False
        self.currently_playing = False

        pygame.init()
        pygame.mixer.init()


    def current_song(self):
        if self.current_index == -1: return "None"
        song = self.mp3_files[self.current_index]
        return song

    def append_event(self, event):
        time_stamp = get_time_stamp()
        current_song = self.current_song()
        entry = [time_stamp, event, current_song]
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
            self.play_next()

    def pause(self):
        if not self.playing_paused:
            pygame.mixer.music.pause()
            self.append_event("Song paused")
            self.playing_paused = True
        else:
            pygame.mixer.music.unpause()
            self.append_event("Song unpaused")
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
                print(event, event.type)
                if event.type == pygame.QUIT: return
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

