import os

class historyLogger:
    def __init__(self):
        self.log_path = './logs/mission_log.txt'
    
    def get_log(self):
        log = []
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                log = f.readlines()
        return log  

    def delete_log(self, index): 
        index = index - 1   
        logs = self.get_log()
        if index < len(logs):
            logs.pop(index)
            with open(self.log_path, 'w') as f:
                for log in logs:
                    f.write(log)
            return True
        else:
            return False

    def clear_log(self):
        with open(self.log_path, 'w') as f:
            f.write('')
    
    def add_log(self, log):
        with open(self.log_path, 'a') as f:
            f.write(log + '\n')

    # f"{self.mission_class},备注:{self.mission_name},{start_time_str} —— {now_time_str},时长{int(time_diff_minute)}分钟\n"
    def history_statistic(self):
        logs = self.get_log()
        logs = [log.strip().split(',') for log in logs]
        # 元组前一项为任务次数，后一项为总时长(min)
        mission_dict = {'数学': (0,0), '英语': (0,0), '编程': (0,0), '运动': (0,0), '娱乐': (0,0), '其他': (0,0)}
        for log in logs:
            mission_class = log[0]
            time = int(log[-1].split('时长')[-1].split('分钟')[0])
            mission_dict[mission_class] = (mission_dict[mission_class][0] + 1, mission_dict[mission_class][1] + time)
        
        return mission_dict
        
