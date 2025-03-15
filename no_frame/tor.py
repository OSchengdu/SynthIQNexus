import os
import time
import requests
from stem import Signal
from stem.control import Controller

def start_tor():
    """启动 Tor 服务"""
    try:
        # 检查 Tor 是否已安装
        if not os.path.exists("/usr/sbin/tor"):
            raise RuntimeError("Tor is not installed. Please install Tor first.")

        # 启动 Tor 服务
        os.system("sudo systemctl start tor")
        time.sleep(5)  # 等待 Tor 启动

        # 验证 Tor 连接
        session = requests.Session()
        session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        response = session.get("https://check.torproject.org")
        if "Congratulations" not in response.text:
            raise RuntimeError("Failed to connect to Tor.")

        print("Tor 连接成功！")
        return session

    except Exception as e:
        print(f"Tor 启动失败：{str(e)}")
        return None

def renew_tor_identity():
    """更换 Tor 出口节点"""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print("Tor 出口节点已更换。")
    except Exception as e:
        print(f"更换 Tor 出口节点失败：{str(e)}")

def stop_tor():
    """停止 Tor 服务"""
    try:
        os.system("sudo systemctl stop tor")
        print("Tor 服务已停止。")
    except Exception as e:
        print(f"停止 Tor 服务失败：{str(e)}")
