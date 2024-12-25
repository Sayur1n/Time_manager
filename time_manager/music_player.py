import os
import threading
from pygame import mixer

class musicPlayer:
    def __init__(self):
        self.music_path = './music/'
        self.stop_point = 0
        self.music_list = self.get_music_list()
        self.thread = None
        self.music_name_on = None

    def get_music_list(self):
        music_list = []
        if os.path.exists(self.music_path):
            music_list = os.listdir(self.music_path)
        return music_list
    

    def play_music(self, music_name):
        if not music_name in self.music_list:
            return False
        if self.music_name_on != music_name:
            self.stop_point = 0
            self.music_name_on = music_name
        
        mixer.init()
        mixer.music.load(os.path.join(self.music_path, music_name))
        mixer.music.play(start = self.stop_point)


        def monitor():
            while mixer.music.get_busy():
                pass
            mixer.music.stop()
            mixer.quit()

        self.thread = threading.Thread(target = monitor)
        self.thread.daemon = True
        self.thread.start()
        return True
    
    def continue_music(self):
        return self.play_music(self.music_name_on)
    
    def pause_music(self):
        if mixer.get_init():
            self.stop_point += mixer.music.get_pos() / 1000.0
            mixer.music.pause()
            return True
        else:
            return False
        