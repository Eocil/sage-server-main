import threading
from sshtunnel import SSHTunnelForwarder

class AutoDL:

    def __init__(self):
        self.ssh_tunnels = {}

    def create_ssh_tunnel(self, host, port, username, password, local_port, remote_host, remote_port, name=""):
        """使用sshtunnel库建立SSH隧道"""
        try:
            print(f"[Server]    - AutoDL-{name} is establishing SSH tunnel...")
            
            # 创建SSH隧道
            tunnel = SSHTunnelForwarder(
                (host, port),
                ssh_username=username,
                ssh_password=password,
                remote_bind_address=(remote_host, remote_port),
                local_bind_address=('127.0.0.1', local_port)
            )
            tunnel.start()  # 启动隧道

            print(f"[Server]    - AutoDL-{name} tunnel is running in the background.")
            # 存储隧道实例，用于后续管理
            self.ssh_tunnels[name] = tunnel

            return tunnel  # 返回隧道对象，表示隧道已启动

        except Exception as e:
            print(f"[Server]    - AutoDL-{name} failed to create tunnel: {e}")
            return False  # 连接失败时返回 False

    def close_ssh_tunnel(self, name):
        """关闭指定隧道并释放资源"""
        if name in self.ssh_tunnels:
            tunnel = self.ssh_tunnels[name]
            tunnel.stop()  # 停止隧道
            print(f"[Server]    - AutoDL-{name} tunnel closed.")
        else:
            print(f"[Server]    - No tunnel found for AutoDL-{name}.")
