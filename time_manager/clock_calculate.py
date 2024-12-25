from math import sin, cos, pi
from datetime import datetime
# 计算指针角度及终止点
def get_clock_hand(center_x, center_y, length1, length2, length3, time):
    '''
    传入圆心坐标、时针长度、分针长度、秒针长度、时间
    得到时针、分针、秒针终点坐标
    '''
    hour = time.hour
    minute = time.minute
    second = time.second

    hour_count = hour % 12
    second_angle = (second * 6) / 180 * pi
    minute_angle = (minute * 6 + second * 0.1) / 180 * pi
    hour_angle = (hour_count * 30 + (minute * 60 + second) / 120) / 180 * pi

    hour_hand_x = center_x + length1 * sin(hour_angle)
    hour_hand_y = center_y - length1 * cos(hour_angle)
    minute_hand_x = center_x + length2 * sin(minute_angle)
    minute_hand_y = center_y - length2 * cos(minute_angle)
    second_hand_x = center_x + length3 * sin(second_angle)
    second_hand_y = center_y - length3 * cos(second_angle)

    return hour_hand_x, hour_hand_y, minute_hand_x, minute_hand_y, second_hand_x, second_hand_y