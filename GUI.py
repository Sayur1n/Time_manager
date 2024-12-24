import numpy as np
import tkinter
import os
from PIL import Image, ImageTk
import time
from datetime import datetime, date

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from clock_calculate import get_clock_hand

class Manager_GUI:
    def __init__(self,root):
        self.root = root
        self.root.title('Your Time Manager')
        self.root.geometry('800x800')
        self.root.resizable(0,0)
        self.root.config(bg='white')
        #self.root.iconbitmap('finger.ico')
        #self.root.protocol('WM_DELETE_WINDOW',self.on_closing)
        self.font_settings = ('宋体', 12)

        self.start_time = 0
        self.mission_on = False
        self.mission_class = None
        self.mission_name = None
        self.tomato_clock = False
        self.tomato_interval = 5
        

        self.create_widgets()

    def create_widgets(self):
        # 创建菜单
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        #filemenu = tk.Menu(menubar,tearoff=0)
        #menubar.add_cascade(label='File', menu=filemenu)
        #filemenu.add_command(label='Exit', command=self.root.quit)

        '''    
        self.file_var = tk.StringVar()
        self.file_var.set('File1')

        tk.Label(self.root, text="选择指纹存档:").pack(pady=10)
        self.save_path_dropdown = ttk.Combobox(self.root, textvariable = self.file_var)
        self.save_path_dropdown['values'] = ('File1', 'File2','File3','File4')
        self.save_path_dropdown.pack()
        '''

        font_settings = ('宋体', 20) 
        # 创建按钮
        self.start_button = tk.Button(self.root, text='开始任务', font = font_settings, command=self.start_mission)
        self.start_button.place(x=600, y=100, width=120, height=80)

        self.stop_button = tk.Button(self.root, text='结束任务', font = font_settings, command=self.stop_mission)
        self.stop_button.place(x=600, y=220, width=120, height=80)


        self.history_button = tk.Button(self.root, text='历史记录', font = font_settings, command=self.history_log)
        self.history_button.place(x=600, y=340, width=120, height=80)
       
        clock_img = Image.open('./images/clock.png')
        if clock_img:
            clock_img = ImageTk.PhotoImage(clock_img)

        self.clock_canvas = tk.Canvas(self.root, width=500, height=500, bg='white')
        self.clock_canvas.place(x=20, y=50)
        self.clock_canvas.image = clock_img  # 保持引用，防止图片丢失
        self.clock_canvas.create_image(250, 250, image = clock_img, anchor='center')
        

        self.info_label = tk.Label(self.root, text='当前无任务', font = ('宋体', 20), bg='white')
        self.time_label = tk.Label(self.root, text='', font = ('宋体', 20), bg='white')
        self.info_label.place(x=200, y=700)
        self.time_label.place(x=200, y=750)

        time_now = datetime.now()
        h_x, h_y, m_x, m_y, s_x, s_y = get_clock_hand(250, 250, 130, 160, 190, time_now)
        self.clock_hour_hand = self.clock_canvas.create_line(250, 250, h_x, h_y, fill='black', width='4',arrow='last', tags='hour')
        self.clock_minute_hand = self.clock_canvas.create_line(250, 250, m_x, m_y, fill='black', width='3',arrow='last', tags='minute')
        self.clock_second_hand = self.clock_canvas.create_line(250, 250, s_x, s_y, fill='black', width='2',arrow='last', tags='second')



        self.start_showing()

    def start_showing(self):
        if self.tomato_clock and (datetime.now() - self.start_time).total_seconds()//60 >= self.tomato_interval:
            self.tomato_clock_trigger()
        self.update_manager()
        self.root.after(10, self.start_showing)  # 递归调用

    def update_manager(self):
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
        messagebox.showinfo("番茄钟提醒", "番茄钟时间到！请休息一会儿。")
        self.tomato_clock = False
        self.tomato_interval = 0
        # 播音乐
        #os.system('start ./music/relaxing_music.mp3')


    def start_mission(self):
        if self.mission_on:
            messagebox.showerror("Error", "请先停止已在进行的任务！")
            return
        # Create a new window
        mission_window = tk.Toplevel(self.root)
        mission_window.title("Choose Mission Details")
        mission_window.geometry("300x350")

        mission_type_var = tk.StringVar()
        finger_var = tk.StringVar()

        # mission type
        tk.Label(mission_window, text="选择任务种类:").pack(pady=10)
        mission_type_dropdown = ttk.Combobox(mission_window, textvariable = mission_type_var)
        mission_type_dropdown['values'] = ('数学', '英语', '编程', '运动', '娱乐', '其他')
        mission_type_dropdown.pack()

        # mission name
        tk.Label(mission_window, text="输入任务名称:(可选)").pack(pady=10)
        mission_name_entry = tk.Entry(mission_window)
        mission_name_entry.pack()

        # create tomato timer choice
        tk.Label(mission_window, text="是否使用番茄钟:").pack(pady=10)
        tomato_frame = tk.Frame(mission_window)
        tomato_frame.pack()
        tomato_var = tk.BooleanVar()
        tk.Radiobutton(tomato_frame, text = "是", variable = tomato_var, value = True).pack(side=tk.LEFT)
        tk.Radiobutton(tomato_frame, text = "否", variable = tomato_var, value = False).pack(side=tk.LEFT)

        tk.Label(mission_window, text="番茄钟时长(min)").pack(pady=10)
        tomato_clock_spinbox = ttk.Spinbox(mission_window, 
            from_=5, 
            to=60,
            increment=5,
            state='readonly',
            width=10)
        tomato_clock_spinbox.set(5)
        tomato_clock_spinbox.pack()

        # Submit button callback
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
            
            self.start_time = datetime.now()
            self.info_label.config(text=f"当前任务:{self.mission_class},备注:{self.mission_name if self.mission_name else '无'}")
            mission_window.destroy()
        
        def quit():
            mission_window.destroy()

        # Add submit button
        submit_button = tk.Button(mission_window, text="确认", command = submit)
        quit_button = tk.Button(mission_window, text="取消", command = quit)
        submit_button.pack(pady=20)
        quit_button.pack(pady=20)
    
    def stop_mission(self):
        if not self.mission_on:
            messagebox.showerror("Error", "当前无任务！")
            return
        time_now = datetime.now()
        time_diff = time_now - self.start_time
        time_diff_minute = time_diff.total_seconds()//60

        # Save the mission log
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

    
    def history_log(self):
        # Create a new window
        history_window = tk.Toplevel(self.root)
        history_window.title("Mission History")
        history_window.geometry("600x600")

        # Read the mission log
        with open('./logs/mission_log.txt', 'r') as f:
            logs = f.readlines()
        
        # Display the logs
        log_labels = []
        for i, log in enumerate(logs):
            temp_log = tk.Label(history_window, text = f'{i}:' + log)
            temp_log.pack(pady=5)
            log_labels.append(temp_log)
        
        # Add a quit button
        def quit():
            history_window.destroy()
        def clear():
            log_labels_to_clear = log_labels
            confirm_window = tk.Toplevel(history_window)
            confirm_window.geometry("300x200")
            confirm_window.title("Clear Mission History")
            history_clear_label = tk.Label(confirm_window, text="确认清空历史记录？")
            history_clear_label.pack(pady=20)
            def confirm():
                confirm_window.destroy()
                with open('./logs/mission_log.txt', 'w') as f:
                    f.write('')
                for log in log_labels_to_clear:
                    log.destroy()
            
            def cancel():
                confirm_window.destroy()
            
            button_frame = tk.Frame(confirm_window)
            button_frame.pack(side=tk.BOTTOM, pady=20)
            # Set button styles
            quit_button = tk.Button(button_frame, text="确认", command=confirm, width=10, height=2, font=('宋体', 12))
            quit_button.pack(side=tk.LEFT, padx=20)
            clear_button = tk.Button(button_frame, text="取消", command=cancel, width=10, height=2, font=('宋体', 12))
            clear_button.pack(side=tk.LEFT, padx=20)


        button_frame = tk.Frame(history_window)
        button_frame.pack(side=tk.BOTTOM, pady=20)
        # Set button styles
        clear_button = tk.Button(button_frame, text="清空", command=clear, width=10, height=2, font=('宋体', 12))
        clear_button.pack(side=tk.LEFT, padx=20)
        quit_button = tk.Button(button_frame, text="退出", command=quit, width=10, height=2, font=('宋体', 12))
        quit_button.pack(side=tk.LEFT, padx=20)




if __name__ == '__main__':
    root = tk.Tk()
    app = Manager_GUI(root)
    root.mainloop()