# 基于 Android 程序模拟蓝牙鼠标实现自动压枪脚本案例

这个项目提供了一个自动化的压枪控制脚本，适用于射击游戏。脚本根据预定义的方向数据模拟鼠标移动，帮助玩家更有效地控制武器后坐力。

## 功能特性

- **自动压枪控制**：脚本根据从文件中读取的后坐力数据自动调整鼠标移动。
- **自定义后坐力模式**：用户可以通过编辑方向数据文件定义自己的后坐力模式。
- **随机偏移**：加入轻微的随机偏移，使得鼠标移动更加自然。
- **UDP 通信**：使用 UDP 将鼠标移动数据发送到指定的 IP 和端口。

## 先决条件

在运行脚本之前，请确保你已经安装了以下内容：

- Python 3.x
- `pywin32` 模块（用于访问 Windows API）
- `socket` 和 `struct`（这两个模块是 Python 标准库的一部分）

你可以使用以下命令通过 pip 安装所需的 Python 包：

```sh
pip install pywin32
```

## 文件结构

```
.
├── main.py               # 自动压枪控制的主脚本
├── PressureInfo
│   └── 200
│       └── main.txt      # 方向数据文件（示例路径）
└── README.md             # 项目 README 文件
```
## 使用方法

1. **调整压枪数据**：

   - 运行 `main.py` 脚本，它会根据 `main.txt` 中的方向数据文件模拟鼠标移动。
   - 你可以通过不断调整 `main.txt` 文件中的 x 和 y 偏移量，使其符合特定武器（例如 AK47）的压枪需求。
   - 每一行的格式应为 `x|y`，其中 `x` 和 `y` 是表示像素移动的整数值。

   `main.txt` 示例：
   ```
   -5|10
   0|15
   5|20
   ```

2. **保存调整后的数据**：

   - 当你对 `main.txt` 中的数据满意时，将文件重命名为对应武器的名称（例如 AK47.txt）。

3. **运行 GUI**：

   - 运行 `gui.py`，你将在界面中看到一个 `AK47` 按钮，选择该按钮后，脚本将自动执行 AK47 的压枪轨迹。

## 注意事项

- 由于脚本依赖 `pywin32` 模块来检测鼠标按键，因此设计为在 Windows 系统上运行。
- 如果发现在游戏中无法正常工作，请尝试以管理员权限运行脚本。
- 脚本使用 UDP 套接字发送鼠标移动数据。如果你不需要此功能，可以修改或删除相关代码部分。



以下是根据你的描述修改后的 README：
使用 `main.py` 脚本调整压枪数据，并将其与 GUI 集成以实现自动压枪功能。你可以根据具体需求进一步调整和扩展此文档。