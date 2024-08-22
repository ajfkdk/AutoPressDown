import socket
import struct
import time
import win32api
import win32con
import random


# 从文件中读取方向数据
def load_direction_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    directions = [tuple(map(int, line.strip().split('|'))) for line in lines if line.strip()]
    return directions


# 模拟鼠标相对移动
def move_mouse(x, y):
    message = struct.pack('!Bii', 0x01, x, y)
    sock.sendto(message, (udp_ip, udp_port))
    print("鼠标左键被按下")

def leftClick():
    message = struct.pack('!B', 0x03)
    sock.sendto(message, (udp_ip, udp_port))
    print("鼠标左键被按下")


# 主压枪逻辑
def auto_recoil_control(directions):
    index = 0
    directions_len = len(directions)

    while True:
        if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000:  # 左键按下
            if index < directions_len:
                x, y = directions[index]
                # 引入随机偏移量
                random_offset_x = random.uniform(-1.0, 1.0)
                x = int(x + random_offset_x * 10)
                # y = int(y * pressForce + random_offset_y * 10)
                move_mouse(x , y*10)
                index += 1
            time.sleep(0.05)  # 控制移动速度，调整这个值以适应你的需求
        else:  # 左键释放
            index = 0
            time.sleep(0.01)


pressForce = 1  # 按下鼠标左键的力度
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_ip = "192.168.8.7"  # 目标UDP IP地址
udp_port = 21115  # 目标UDP端口

if __name__ == "__main__":
    file_path = r"C:\Users\pc\PycharmProjects\pythonProject\autoPressDown\PressureInfo\200\main.txt"  # 你的方向数据文件路径

    directions = load_direction_data(file_path)

    auto_recoil_control(directions)
