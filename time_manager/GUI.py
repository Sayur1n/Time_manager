import os
from PIL import Image, ImageTk
import time
from datetime import datetime, date

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from clock_calculate import get_clock_hand
from history_logger import historyLogger
from music_player import musicPlayer

from tkinter import filedialog
import shutil

class Manager_GUI:
    def __init__(self,root):
        # 初始化窗口
        self.root = root
        self.root.title('Your Time Manager')
        self.root.geometry('800x800')
        self.root.resizable(0,0)
        self.root.config(bg='white')
        self.font_settings = ('宋体', 12)

        # 任务有关变量初始化
        self.start_time = 0
        self.mission_on = False
        self.mission_class = None
        self.mission_name = None
        self.tomato_clock = False
        self.tomato_interval = 5
        self.mission_types = ['数学', '英语', '编程', '运动', '娱乐', '其他']

        # 初始化日志记录器和音乐播放器
        self.history_logger = historyLogger()
        self.music_player = musicPlayer()
        self.music_on = False

        self.create_widgets()

    def create_widgets(self):
        # 创建菜单
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        font_settings = ('宋体', 20) 

        # 创建按钮
        self.start_button = tk.Button(self.root, text='开始任务', font = font_settings, command=self.start_mission)
        self.start_button.place(x=600, y=50, width=120, height=80)

        self.stop_button = tk.Button(self.root, text='结束任务', font = font_settings, command=self.stop_mission)
        self.stop_button.place(x=600, y=170, width=120, height=80)

        self.history_button = tk.Button(self.root, text='历史记录', font = font_settings, command=self.history_log)
        self.history_button.place(x=600, y=290, width=120, height=80)

        self.music_button = tk.Button(self.root, text='音乐播放', font = font_settings, command=self.music)
        self.music_button.place(x=600, y=410, width=120, height=80)

        self.music_stop_button = tk.Button(self.root, text='音乐暂停', font = font_settings, command=self.music_stop)
        self.music_stop_button.place(x=600, y=530, width=120, height=80)

        # 创建钟表
        clock_img = Image.open('./images/clock.png')
        if clock_img:
            clock_img = ImageTk.PhotoImage(clock_img)

        self.clock_canvas = tk.Canvas(self.root, width=500, height=500, bg='white')
        self.clock_canvas.place(x=20, y=50)
        self.clock_canvas.image = clock_img  # 保持引用，防止图片丢失
        self.clock_canvas.create_image(250, 250, image = clock_img, anchor='center')
        # 初始化表针位置
        time_now = datetime.now()
        h_x, h_y, m_x, m_y, s_x, s_y = get_clock_hand(250, 250, 130, 160, 190, time_now)
        self.clock_hour_hand = self.clock_canvas.create_line(250, 250, h_x, h_y, fill='black', width='4',arrow='last', tags='hour')
        self.clock_minute_hand = self.clock_canvas.create_line(250, 250, m_x, m_y, fill='black', width='3',arrow='last', tags='minute')
        self.clock_second_hand = self.clock_canvas.create_line(250, 250, s_x, s_y, fill='black', width='2',arrow='last', tags='second')

        # 创建提示信息
        self.info_label = tk.Label(self.root, text='当前无任务', font = font_settings, bg='white')
        self.time_label = tk.Label(self.root, text='', font = font_settings, bg='white')
        self.music_label = tk.Label(self.root, text='', font = font_settings, bg='white')
        self.info_label.place(x=200, y=650)
        self.time_label.place(x=200, y=700)
        self.music_label.place(x=200, y=750)

        self.start_showing()

    def start_showing(self):
        '''
        递归式调用，每10ms更新一次界面，来保证界面的实时更新和番茄钟的触发
        '''
        if self.tomato_clock and (datetime.now() - self.start_time).total_seconds() >= self.tomato_interval:
            self.tomato_clock_trigger()
        self.update_manager()
        self.root.after(10, self.start_showing)

    def update_manager(self):
        '''
        更新界面信息
        '''
        time_now = datetime.now()
        # 更新文字
        if self.mission_on:
            time_diff = time_now - self.start_time
            time_diff_minute = time_diff.total_seconds()//60
            self.time_label.config(text=f"已进行{int(time_diff_minute)}分钟")
        
        # 更新钟表
        h_x, h_y, m_x, m_y, s_x, s_y = get_clock_hand(250, 250, 130, 160, 190, time_now)
        self.clock_canvas.delete('hour')
        self.clock_canvas.delete('minute')
        self.clock_canvas.delete('second')
        self.clock_hour_hand = self.clock_canvas.create_line(250, 250, h_x, h_y, fill='black', width='4', arrow='last', tags='hour')
        self.clock_minute_hand = self.clock_canvas.create_line(250, 250, m_x, m_y, fill='black', width='3', arrow='last', tags='minute')
        self.clock_second_hand = self.clock_canvas.create_line(250, 250, s_x, s_y, fill='black', width='2', arrow='last', tags='second')
        
    def tomato_clock_trigger(self):
        '''
        番茄钟触发及弹窗提醒
        '''
        self.music_player.alarm_clock_on()
        messagebox.showinfo("番茄钟提醒", "番茄钟时间到！请休息一会儿。")
        self.tomato_clock = False
        self.tomato_interval = 0
        self.music_player.alarm_clock_off()
        # 对正在播放的音乐，继续播放
        if self.music_on:
            time.sleep(0.1)
            self.music_player.continue_music()
        
    def music(self):
        '''
        选择音乐界面
        '''
        music_window = tk.Toplevel(self.root)
        music_window.title("Choose Music")
        music_window.geometry("400x150")
        music_window.resizable(0,0)
        music_window.grab_set()

        music_var = tk.StringVar()

        # 选择音乐
        tk.Label(music_window, text="选择音乐:").pack(pady=10)
        music_dropdown = ttk.Combobox(music_window, textvariable = music_var)
        music_paths = self.music_player.get_music_list()
        music_names = [name.split('.mp3')[0] for name in music_paths if name.endswith('.mp3')]
        music_dropdown['values'] = music_names
        music_dropdown.pack()

        # 确认键回调函数
        def submit():
            music_name = music_dropdown.get()
            if not music_name:
                messagebox.showerror("Error", "请选择音乐！")
                music_window.lift()  # 将窗口置于顶层
                music_window.focus_force()
                return
            # 暂停当前音乐，停止0.1s防止音乐播放冲突
            self.music_player.pause_music()
            music_window.destroy()
            time.sleep(0.1)
            if not self.music_on:
                self.music_stop_button.config(text='音乐暂停')

            if not self.music_player.play_music(music_name + '.mp3'):
                messagebox.showerror("Error", "没有该音乐！")
                return
            else:
                self.music_on = True
                self.music_label.config(text=f"当前音乐:{music_name}")

        # 取消键回调函数
        def quit():
            music_window.destroy()
        
        # 加载音乐文件
        def load():
            music_file = filedialog.askopenfilename(
                title='选择音乐文件',
                filetypes=[('MP3 Files', '*.mp3')]
            )

            if music_file:
                # 将文件复制到music文件夹下
                dest = os.path.join('./music', os.path.basename(music_file))
                shutil.copy2(music_file, dest)
                
                # 刷新音乐列表
                music_paths = self.music_player.get_music_list()
                music_names = [name.split('.mp3')[0] for name in music_paths if name.endswith('.mp3')]
                music_dropdown['values'] = music_names
                
                messagebox.showinfo("成功", "音乐文件已加载")
                music_window.lift()  # 将窗口置于顶层
                music_window.focus_force()


        # 按钮设置
        button_frame = tk.Frame(music_window)
        button_frame.pack(side=tk.BOTTOM, pady=20)
        
        submit_button = tk.Button(button_frame, text="确认", command = submit, width=10, height=2, font=('宋体', 12))
        quit_button = tk.Button(button_frame, text="取消", command = quit, width=10, height=2, font=('宋体', 12))
        load_button = tk.Button(button_frame, text="添加音乐", command = load, width=10, height=2, font=('宋体', 12))
        submit_button.pack(side=tk.LEFT, padx=20)
        quit_button.pack(side=tk.LEFT, padx=20)
        load_button.pack(side=tk.BOTTOM, padx=20)
    
    def music_stop(self):
        '''
        暂停/继续音乐键回调函数
        '''
        if self.music_on:
            if self.music_player.pause_music():
                self.music_on = False
                self.music_stop_button.config(text='音乐继续')
        else:
            if self.music_player.continue_music():
                self.music_on = True
                self.music_stop_button.config(text='音乐暂停')


    def start_mission(self):
        '''
        开始任务界面
        '''
        if self.mission_on:
            messagebox.showerror("Error", "请先停止已在进行的任务！")
            return
        
        mission_window = tk.Toplevel(self.root)
        mission_window.title("Choose Mission Details")
        mission_window.geometry("300x350")
        mission_window.resizable(0,0)
        mission_window.grab_set()

        # 选择任务类型
        mission_type_var = tk.StringVar()
        tk.Label(mission_window, text="选择任务种类:").pack(pady=10)
        mission_type_dropdown = ttk.Combobox(mission_window, textvariable = mission_type_var)
        mission_type_dropdown['values'] = self.mission_types
        mission_type_dropdown.pack()

        # 设置备注
        tk.Label(mission_window, text="输入任务名称:(可选)").pack(pady=10)
        mission_name_entry = tk.Entry(mission_window)
        mission_name_entry.pack()

        # 番茄钟
        tk.Label(mission_window, text="是否使用番茄钟:").pack(pady=10)
        tomato_frame = tk.Frame(mission_window)
        tomato_frame.pack()
        tomato_var = tk.BooleanVar()
        tk.Radiobutton(tomato_frame, text = "是", variable = tomato_var, value = True).pack(side=tk.LEFT)
        tk.Radiobutton(tomato_frame, text = "否", variable = tomato_var, value = False).pack(side=tk.LEFT)

        tk.Label(mission_window, text="番茄钟时长(min)").pack(pady=10)
        # 设置番茄钟时长，固定长度间隔，默认为5
        tomato_clock_spinbox = ttk.Spinbox(mission_window, 
            from_=5, 
            to=120,
            increment=5,
            state='readonly',
            width=10)
        tomato_clock_spinbox.set(5)
        tomato_clock_spinbox.pack()

        # 确认键回调函数
        def submit():

            mission_class = mission_type_dropdown.get()
            mission_name = mission_name_entry.get()
            if not mission_class:
                messagebox.showerror("Error", "请选择任务类型！")
                return
            self.mission_on = True
            self.mission_class = mission_class
            self.mission_name = mission_name
            self.tomato_clock = tomato_var.get()
            self.tomato_interval = int(tomato_clock_spinbox.get())
            
            # 更新界面信息
            self.start_time = datetime.now()
            self.info_label.config(text=f"当前任务:{self.mission_class},备注:{self.mission_name if self.mission_name else '无'}")
            mission_window.destroy()
        
        def quit():
            mission_window.destroy()


        # 按钮设置
        button_frame = tk.Frame(mission_window)
        button_frame.pack(side=tk.BOTTOM, pady=20)
        
        submit_button = tk.Button(button_frame, text="确认", command = submit, width=10, height=2, font=('宋体', 12))
        quit_button = tk.Button(button_frame, text="取消", command = quit, width=10, height=2, font=('宋体', 12))
        submit_button.pack(side=tk.LEFT, padx=20)
        quit_button.pack(side=tk.LEFT, padx=20)
    
    def stop_mission(self):
        '''
        结束任务界面
        '''
        if not self.mission_on:
            messagebox.showerror("Error", "当前无任务！")
            return
        
        # 计算时间差
        time_now = datetime.now()
        time_diff = time_now - self.start_time
        time_diff_minute = time_diff.total_seconds()//60

        # 存储任务记录
        with open('./logs/mission_log.txt', 'a') as f:
            start_time_str = self.start_time.strftime("%Y-%m-%d %H:%M:%S")
            now_time_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{self.mission_class},备注:{self.mission_name},{start_time_str} —— {now_time_str},时长{int(time_diff_minute)}分钟\n")
        
        self.mission_on = False
        self.mission_class = None
        self.mission_name = None
        self.tomato_clock = False
        self.tomato_interval = 0
        self.info_label.config(text='当前无任务')
        self.time_label.config(text='')

    # 查看任务历史记录
    def history_log(self):
        font_settings = ('宋体', 18)
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Mission History")
        history_window.geometry("800x800")
        history_window.resizable(0,0)
        history_window.grab_set()

        # 读取历史记录
        logs = self.history_logger.get_log()
        
        frame = tk.Frame(history_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # 创建一个 Text 小部件用于显示日志，并添加滚动条
        text_widget = tk.Text(frame, wrap=tk.WORD, font = self.font_settings)
        scrollbar = tk.Scrollbar(frame, command = text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        # 放置滚动条和 Text 小部件
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 将日志内容插入到 Text 小部件中
        for i, log in enumerate(logs):
            text_widget.insert(tk.END, f"{i+1:2d}: {log}\n")
        text_widget.config(state=tk.DISABLED)
        
       
        def quit():
            history_window.destroy()
        
        # 删除任务记录回调函数
        def delete():
            logs_length = len(logs)
            delete_window = tk.Toplevel(history_window)
            delete_window.geometry("350x200")
            delete_window.title("Delete Mission History")
            delete_window.grab_set()
            delete_window.resizable(0,0)

            tk.Label(delete_window, text="输入要删除的任务编号:", font = font_settings).pack(pady=10)
            mission_name_entry = tk.Entry(delete_window)
            mission_name_entry.pack()

            def confirm():
                try:
                    mission_idx = int(mission_name_entry.get())
                    if mission_idx < 1 or mission_idx > logs_length:
                        messagebox.showerror("Error", "任务编号超出范围！")
                        return
                    self.history_logger.delete_log(mission_idx)
                    delete_window.destroy()

                    # 更新记录显示
                    logs = self.history_logger.get_log()
                    text_widget.config(state=tk.NORMAL) 
                    text_widget.delete(1.0, tk.END)
                    for i, log in enumerate(logs):
                        text_widget.insert(tk.END, f"{i+1:2d}: {log}\n")
                    text_widget.config(state=tk.DISABLED)

                    # 更新统计信息
                    statistics_data = self.history_logger.history_statistic()
                    for i in range(len(self.mission_types)):
                        statistics_labels[i].config(text=f"{self.mission_types[i]}: {statistics_data[self.mission_types[i]][0]}次, 总时长{statistics_data[self.mission_types[i]][1]}分钟", font = self.font_settings)

                except ValueError:
                    messagebox.showerror("Error", "请输入整数！")
                    return
                
            def cancel():
                delete_window.destroy()
            
            # 按钮设置
            delete_button_frame = tk.Frame(delete_window)
            delete_button_frame.pack(side=tk.BOTTOM, pady=20)
    
            delete_confirm_button = tk.Button(delete_button_frame, text="确认", command=confirm, width=10, height=2, font = font_settings)
            delete_confirm_button.pack(side=tk.LEFT, padx=20)
            delete_cancel_button = tk.Button(delete_button_frame, text="取消", command=cancel, width=10, height=2, font = font_settings)
            delete_cancel_button.pack(side=tk.LEFT, padx=20)
            
        # 清空任务记录回调函数
        def clear():
            confirm_window = tk.Toplevel(history_window)
            confirm_window.geometry("350x200")
            confirm_window.title("Clear Mission History")
            confirm_window.grab_set()   # 阻止与其他窗口的交互

            history_clear_label = tk.Label(confirm_window, text="确认清空历史记录？",font = font_settings)
            history_clear_label.pack(pady=20)
            def confirm():
                confirm_window.destroy()
                self.history_logger.clear_log()
                text_widget.config(state=tk.NORMAL)  # 先将状态改为可编辑
                text_widget.delete(1.0, tk.END)  # 清除从第1行第0列到最后的内容
                text_widget.config(state=tk.DISABLED)  # 恢复为只读状态

                # 重置统计信息
                for i ,label in enumerate(statistics_labels):
                    name = self.mission_types[i]
                    label.config(text=f"{name}: {0}次, 总时长{0}分钟", font = font_settings)
            
            def cancel():
                confirm_window.destroy()
            
            # 按钮设置
            clear_button_frame = tk.Frame(confirm_window)
            clear_button_frame.pack(side=tk.BOTTOM, pady=20)
            
            clear_confirm_button = tk.Button(clear_button_frame, text="确认", command=confirm, width=10, height=2, font = font_settings)
            clear_confirm_button.pack(side=tk.LEFT, padx=20)
            clear_cancel_button = tk.Button(clear_button_frame, text="取消", command=cancel, width=10, height=2, font = font_settings)
            clear_cancel_button.pack(side=tk.LEFT, padx=20)

        # 统计信息
        statistics_frame = tk.Frame(history_window)
        statistics_frame.pack(side=tk.BOTTOM, pady=20)
        statistics_data = self.history_logger.history_statistic()
        statistics_labels = []
        
        tk.Label(statistics_frame, text="统计数据：", font = font_settings).pack(pady=5)
        for name, tup in statistics_data.items():
            statistics_labels.append(tk.Label(statistics_frame, text=f"{name}: {tup[0]}次, 总时长{tup[1]}分钟", font = font_settings))
            statistics_labels[-1].pack(pady=5)

        # 按钮设置
        button_frame = tk.Frame(history_window)
        button_frame.pack(side=tk.BOTTOM, pady=20)

        delete_button = tk.Button(button_frame, text="删除", command = delete, width=10, height=2, font = font_settings)
        delete_button.pack(side=tk.LEFT, padx=20)
        clear_button = tk.Button(button_frame, text="清空", command = clear, width=10, height=2, font = font_settings)
        clear_button.pack(side=tk.LEFT, padx=20)
        quit_button = tk.Button(button_frame, text="退出", command = quit, width=10, height=2, font = font_settings)
        quit_button.pack(side=tk.LEFT, padx=20)


if __name__ == '__main__':
    root = tk.Tk()
    app = Manager_GUI(root)
    root.mainloop()

