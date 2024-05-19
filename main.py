from pynput import mouse
import pyautogui
import tkinter as tk
import time

# 说明
print("点按鼠标左键，将以当前坐标为中心截取1024x1024的图像。\n按下 Ctrl+C 停止监听并退出程序。")

# 定义一个透明的窗口，让它的大小与屏幕一样：

root = tk.Tk()
root.overrideredirect(True)  # 隐藏窗口的标题栏
root.attributes("-alpha", 0.1)  # 窗口透明度10%
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg="black")

# 定义初始鼠标坐标
c_x = 0
c_y = 0


# 获取当前鼠标坐标
# 函数，单击左键后执行

def on_click(x, y, button, pressed):
    """鼠标点击事件的回调函数"""
    # 设置全局变量用来方便赋值
    global c_x, c_y
    if pressed:
        # 当鼠标被按下时，打印并记录坐标
        print(f"Mouse clicked at coordinates: ({x}, {y})")
        c_x = x
        c_y = y
        # 阻止截图超出最小范围
        if c_x < 512:
            c_x = 512
        if c_y < 512:
            c_y = 512
        # 停止监听
        return False


# 设置监听器
listener = mouse.Listener(on_click=on_click)
listener.start()

try:
    listener.join()
    # 执行截图操作
    # 起点x,起点y,宽度w,高度h
    img = pyautogui.screenshot(region=[c_x - 512, c_y - 512, 1024, 1024])

    # 销毁透明窗口
    root.destroy()

    # 获取当前时间
    current_time = time.time()

    # 将时间戳转换为格式化的时间字符串
    formatted_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(current_time))

    img.save(f"screenshot{formatted_time}.png")

except KeyboardInterrupt:
    # 允许通过 Ctrl+C 停止监听并退出
    listener.stop()
