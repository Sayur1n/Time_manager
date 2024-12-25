import os
import threading
from pygame import mixer
import time

class musicPlayer:
    def __init__(self):
        self.music_path = './music/'
        self.stop_point = 0
        self.music_list = self.get_music_list()
        self.thread = None
        self.music_name_on = None
        self.alarm_clock = 'alarm_clock.mp3'

    def get_music_list(self):
        '''
        获取音乐列表
        '''
        music_list = []
        # 读取音乐，对于闹钟音乐，单独处理
        if os.path.exists(self.music_path):
            music_list = os.listdir(self.music_path)
            clock_idx = music_list.index('alarm_clock.mp3')
            self.alarm_clock = music_list.pop(clock_idx)
        return music_list
    
    def play_music(self, music_name): # 这里的music_name带后缀
        '''
        播放音乐
        '''
        # 若不为闹钟音乐，继续播放
        if music_name != self.alarm_clock:
            if music_name not in self.music_list:
                return False
            if self.music_name_on != music_name:
                self.stop_point = 0
                self.music_name_on = music_name
            
            mixer.init()
            mixer.music.load(os.path.join(self.music_path, music_name))
            mixer.music.play(start = self.stop_point)
        # 若为闹钟音乐，从头播放
        else:
            mixer.init()
            mixer.music.load(os.path.join(self.music_path, music_name))
            mixer.music.play()

        # 监视函数，当音乐暂停时即停止mixer
        def monitor():
            while mixer.music.get_busy():
                pass
            mixer.music.stop()
            mixer.quit()

        # 独立线程监视音乐播放
        self.thread = threading.Thread(target = monitor)
        self.thread.daemon = True
        self.thread.start()
        return True
    
    def continue_music(self):
        '''
        继续播放音乐
        '''
        return self.play_music(self.music_name_on)
    
    def pause_music(self):
        '''
        暂停音乐并记录暂停点
        '''
        if mixer.get_init():
            # 对同一首歌，暂停点的记录应当累加
            self.stop_point += mixer.music.get_pos() / 1000.0
            mixer.music.pause()
            return True
        else:
            return False
    
    def alarm_clock_on(self):
        '''
        开启闹钟
        '''
        self.pause_music()
        time.sleep(0.2)
        return self.play_music(self.alarm_clock)
    
    def alarm_clock_off(self):
        '''
        关闭闹钟
        '''
        if mixer.get_init():
            mixer.music.pause()
            return True
        else:
            return False
        