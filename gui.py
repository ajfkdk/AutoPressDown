import os
import random
import socket
import struct
import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import win32api
import win32con
from PIL import Image, ImageTk
import sys

class AutoRecoilControl:
    def __init__(self, directions, pressForce, udp_ip, udp_port):
        self.directions = directions
        self.pressForce = pressForce
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.alt_toggle = False
        self.lock = threading.Lock()

    def move_mouse(self, x, y):
        if not self.alt_toggle:
            message = struct.pack('!Bii', 0x01, x, y)
            self.sock.sendto(message, (self.udp_ip, self.udp_port))
            print("鼠标移动: ", x, y)
        else:
            print("Alt键切换为停止状态，停止鼠标移动")

    def auto_recoil_control(self):
        index = 0

        while self.running:
            with self.lock:
                directions_len = len(self.directions)
                current_directions = self.directions

            if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000:  # 左键按下
                if index < directions_len:
                    x, y = current_directions[index]
                    # 引入随机偏移量
                    random_offset_x = random.uniform(-1.0, 1.0)
                    x = int(x + random_offset_x * 10)
                    self.move_mouse(x, y * 10)
                    index += 1
                time.sleep(0.05)  # 控制移动速度，调整这个值以适应你的需求
            else:  # 左键释放
                index = 0
                time.sleep(0.01)

    def start(self):
        self.running = True
        threading.Thread(target=self.auto_recoil_control).start()

    def stop(self):
        self.running = False

    def update_directions(self, new_directions):
        with self.lock:
            self.directions = new_directions

def load_direction_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    directions = [tuple(map(int, line.strip().split('|'))) for line in lines if line.strip()]
    return directions

def open_file_selection_gui(selected_folder, control):
    global root, bg_photo
    root = tk.Tk()
    root.title("选择配置文件")
    root.geometry("600x400")  # 固定窗口大小
    root.resizable(False, False)  # 禁止调整窗口大小
    root.attributes("-topmost", True)  # 使窗口总是置顶

    # 设置背景图片
    bg_image_path = r"C:\Users\pc\PycharmProjects\pythonProject\autoPressDown\img.png"
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((600, 400), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack(fill='both', expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor='nw')

    # 创建滚动条和可滚动框架
    scrollable_frame = tk.Frame(canvas, bg='')

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    files = [f for f in os.listdir(selected_folder) if f.endswith('.txt')]

    # 自定义按钮样式
    button_font = ('Helvetica', 12)
    button_foreground = 'white'
    button_background = '#333333'
    button_active_background = '#666666'

    # 使用grid布局并排显示按钮
    for idx, file in enumerate(files):
        file_path = os.path.join(selected_folder, file)

        # 创建带透明背景的Label作为按钮
        btn_frame = tk.Frame(scrollable_frame, bg='', bd=0)
        btn_frame.grid(row=idx // 4, column=idx % 4, padx=10, pady=5, sticky='ew')

        btn = tk.Label(btn_frame, text=file, font=button_font, fg=button_foreground,
                       bg=button_background, bd=2, relief="raised", cursor="hand2")
        btn.pack(fill='both', expand=True)
        btn.bind("<Button-1>", lambda e, fp=file_path: on_file_selected(fp, control))
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=button_active_background))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=button_background))

    root.mainloop()

def on_file_selected(file_path, control):
    control.stop()  # 停止当前的压枪控制
    time.sleep(0.1)  # 确保线程已经停止
    directions = load_direction_data(file_path)
    control.update_directions(directions)
    control.start()
    root.destroy()

def listen_for_keys(selected_folder, control):
    alt_state = False

    while True:
        if win32api.GetAsyncKeyState(0x12) & 0x8000:  # Alt 键的虚拟键码是 0x12
            if not alt_state:
                control.alt_toggle = not control.alt_toggle
                print(f"Alt键切换: {'停止' if control.alt_toggle else '开始'}")
                alt_state = True
        else:
            alt_state = False

        if win32api.GetAsyncKeyState(0x5A) & 0x8000:  # Z 键的虚拟键码是 0x5A
            open_file_selection_gui(selected_folder, control)
        if win32api.GetAsyncKeyState(0x58) & 0x8000:  # X 键的虚拟键码是 0x58
            control.stop()
            sys.exit()  # 关闭程序
        time.sleep(0.1)

def select_sensitivity_folder(control):
    root = tk.Tk()
    root.title("选择鼠标灵敏度文件夹")
    root.geometry("400x300")
    root.attributes("-topmost", True)

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    folders = [f for f in os.listdir(file_dir) if os.path.isdir(os.path.join(file_dir, f))]

    def on_folder_selected(folder_path, control):
        global selected_folder
        selected_folder = folder_path
        root.destroy()
        open_file_selection_gui(selected_folder, control)

    for folder in folders:
        folder_path = os.path.join(file_dir, folder)
        btn = tk.Button(scrollable_frame, text=folder, command=lambda fp=folder_path: on_folder_selected(fp, control))
        btn.pack(fill=tk.X, padx=10, pady=5)

    root.mainloop()

# 初始配置
pressForce = 1  # 按下鼠标左键的力度
udp_ip = "192.168.8.7"  # 目标UDP IP地址
udp_port = 21115  # 目标UDP端口
file_dir = r"C:\Users\pc\PycharmProjects\pythonProject\autoPressDown\PressureInfo"  # 配置文件目录

if __name__ == "__main__":
    selected_folder = None
    control = AutoRecoilControl([], pressForce, udp_ip, udp_port)
    select_sensitivity_folder(control)
    file_path = os.path.join(selected_folder, "main.txt")  # 默认方向数据文件路径
    directions = load_direction_data(file_path)
    control.update_directions(directions)

    control.start()

    listen_for_keys(selected_folder, control)