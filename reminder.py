import json
import time
import os
import sys
import ctypes
import threading
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# 配置文件路径
CONFIG_PATH = Path(__file__).parent / "config.json"

# 默认配置
DEFAULT_CONFIG = {
    "reminder_text": "该休息一下啦，活动活动身体~",
    "reminder_interval": 30,  # 分钟
    "shutdown_time": None,  # 格式："22:30"，设置为None则不自动关机
    "popup_title": "温馨提醒"
}

def load_config():
    """加载配置文件"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 创建默认配置文件
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print(f"配置文件已保存到: {CONFIG_PATH}")

def show_popup(title, message):
    """显示弹窗提醒"""
    try:
        # Windows系统弹窗
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1000)  # MB_ICONINFORMATION | MB_SYSTEMMODAL
    except Exception as e:
        print(f"弹窗失败: {e}")

def shutdown_system():
    """执行系统关机"""
    try:
        if os.name == 'nt':  # Windows
            os.system("shutdown /s /t 60 /c \"到点自动关机啦，60秒后将关闭计算机\"")
        else:  # Linux/macOS
            os.system("shutdown -h +1 \"到点自动关机啦，1分钟后将关闭计算机\"")
        print("已触发自动关机，系统将在1分钟后关闭")
    except Exception as e:
        print(f"关机失败: {e}")

def reminder_loop(config):
    """提醒循环"""
    interval = config['reminder_interval'] * 60  # 转换为秒
    print(f"提醒服务已启动，每{config['reminder_interval']}分钟弹出提醒")
    while True:
        time.sleep(interval)
        show_popup(config['popup_title'], config['reminder_text'])

def shutdown_monitor(config):
    """关机监控线程"""
    shutdown_time = config.get('shutdown_time')
    if not shutdown_time:
        print("未配置自动关机时间，关机监控未启动")
        return
    
    print(f"关机监控已启动，将在每天{shutdown_time}自动关机")
    while True:
        now = datetime.now()
        target_time = datetime.strptime(shutdown_time, "%H:%M").time()
        current_time = now.time()
        
        # 如果当前时间已经超过目标时间，计算明天的目标时间
        if current_time >= target_time:
            next_shutdown = (now + timedelta(days=1)).replace(
                hour=target_time.hour,
                minute=target_time.minute,
                second=0,
                microsecond=0
            )
        else:
            next_shutdown = now.replace(
                hour=target_time.hour,
                minute=target_time.minute,
                second=0,
                microsecond=0
            )
        
        # 计算等待时间
        wait_seconds = (next_shutdown - now).total_seconds()
        time.sleep(wait_seconds)
        
        # 执行关机
        show_popup("关机提醒", f"到点自动关机啦，系统将在1分钟后关闭")
        shutdown_system()
        # 关机执行后等待2分钟避免重复触发
        time.sleep(120)

def run_background(config):
    """后台运行服务"""
    print("提醒服务正在启动...")
    
    # 启动提醒线程
    reminder_thread = threading.Thread(target=reminder_loop, args=(config,), daemon=True)
    reminder_thread.start()
    
    # 启动关机监控线程
    shutdown_thread = threading.Thread(target=shutdown_monitor, args=(config,), daemon=True)
    shutdown_thread.start()
    
    print("服务已成功挂载到后台运行")
    print(f"提醒间隔: {config['reminder_interval']}分钟")
    print(f"提醒内容: {config['reminder_text']}")
    if config.get('shutdown_time'):
        print(f"自动关机时间: 每天{config['shutdown_time']}")
    print("按Ctrl+C可以停止服务")
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\n服务已停止")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="定时提醒与自动关机工具")
    parser.add_argument('--config', action='store_true', help='生成默认配置文件')
    parser.add_argument('--run', action='store_true', help='启动提醒服务')
    parser.add_argument('--set-text', type=str, help='设置提醒文字')
    parser.add_argument('--set-interval', type=int, help='设置提醒间隔(分钟)')
    parser.add_argument('--set-shutdown', type=str, help='设置自动关机时间，格式HH:MM，设置为none则取消')
    parser.add_argument('--test-popup', action='store_true', help='测试弹窗功能')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    if args.config:
        load_config()  # 加载时会自动创建默认配置
        return
    
    config = load_config()
    
    if args.set_text:
        config['reminder_text'] = args.set_text
        save_config(config)
        print(f"提醒文字已设置为: {args.set_text}")
        return
    
    if args.set_interval:
        if args.set_interval < 1:
            print("提醒间隔不能小于1分钟")
            return
        config['reminder_interval'] = args.set_interval
        save_config(config)
        print(f"提醒间隔已设置为: {args.set_interval}分钟")
        return
    
    if args.set_shutdown:
        if args.set_shutdown.lower() == 'none':
            config['shutdown_time'] = None
            save_config(config)
            print("已取消自动关机")
        else:
            try:
                # 验证时间格式
                datetime.strptime(args.set_shutdown, "%H:%M")
                config['shutdown_time'] = args.set_shutdown
                save_config(config)
                print(f"自动关机时间已设置为: 每天{args.set_shutdown}")
            except ValueError:
                print("时间格式错误，请使用HH:MM格式，例如 22:30")
        return
    
    if args.test_popup:
        print("正在测试弹窗...")
        show_popup(config['popup_title'], config['reminder_text'])
        print("弹窗测试完成")
        return
    
    if args.run:
        run_background(config)
        return

if __name__ == "__main__":
    main()
