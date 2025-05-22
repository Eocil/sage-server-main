import queue
import sys
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
import threading
import time
from typing import Dict, Any, Optional, Tuple
import os


class Jupyter:
    def __init__(self, conda_env: str = "jupyter", timeout: int = 60):
        """
        初始化Jupyter Kernel包装器

        Args:
            conda_env: Conda环境名称
            timeout: 执行超时时间(秒)
        """
        self.timeout = timeout
        self.kernel_manager = None
        self.kernel_client = None
        self.conda_env = conda_env
        self._init_kernel()

    def _init_kernel(self):
        """初始化kernel连接"""
        # 如果指定了conda环境,设置对应的python解释器
        if self.conda_env:
            import tempfile
            import json
            import shutil

            conda_prefix = os.path.join(
                os.path.expanduser("~"), "miniconda3", "envs", self.conda_env
            )
            python_path = os.path.join(conda_prefix, "python.exe")

            # 创建临时kernel spec
            kernel_spec_manager = KernelSpecManager()
            kernel_name = f"python-{self.conda_env}"

            kernel_json = {
                "argv": [
                    python_path,
                    "-m",
                    "ipykernel_launcher",
                    "-f",
                    "{connection_file}",
                ],
                "display_name": f"Python ({self.conda_env})",
                "language": "python",
            }

            # 创建临时目录存放kernel配置
            temp_dir = tempfile.mkdtemp()
            try:
                # 写入kernel.json
                os.makedirs(
                    os.path.join(temp_dir, "kernels", kernel_name), exist_ok=True
                )
                kernel_json_file = os.path.join(
                    temp_dir, "kernels", kernel_name, "kernel.json"
                )
                with open(kernel_json_file, "w") as f:
                    json.dump(kernel_json, f)

                # 安装kernel spec
                kernel_spec_manager.install_kernel_spec(
                    os.path.join(temp_dir, "kernels", kernel_name),
                    kernel_name=kernel_name,
                    user=True,
                )
            finally:
                # 清理临时目录
                shutil.rmtree(temp_dir)

            self.kernel_manager = KernelManager(kernel_name=kernel_name)
        else:
            self.kernel_manager = KernelManager()

        self.kernel_manager.start_kernel()
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()

    def _collect_outputs(self, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        收集kernel执行的所有输出

        Returns:
            包含不同类型输出的字典
        """
        outputs = {
            "text": [],  # 执行结果
            "error": None,  # 错误信息
            "images": [],  # 图片输出
            "other": [],  # 其他输出
        }

        timeout = timeout or self.timeout
        deadline = time.time() + timeout

        while True:
            try:
                msg = self.kernel_client.get_iopub_msg(timeout=1)
                if msg["header"]["msg_type"] == "status":
                    if msg["content"]["execution_state"] == "idle":
                        break
                elif msg["header"]["msg_type"] == "stream":
                    outputs["text"].append(msg["content"]["text"])
                elif msg["header"]["msg_type"] == "execute_result":
                    if "text/plain" in msg["content"]["data"]:
                        outputs["text"].append(msg["content"]["data"]["text/plain"])
                    else:
                        outputs["other"].append(msg["content"]["data"])

                elif msg["header"]["msg_type"] == "error":
                    outputs["error"] = "\n".join(msg["content"]["traceback"])
                elif msg["header"]["msg_type"] == "display_data":
                    if "image/png" in msg["content"]["data"]:
                        outputs["images"].append(msg["content"]["data"]["image/png"])
                    else:
                        outputs["other"].append(msg["content"]["data"])

                if time.time() > deadline:
                    self.interrupt()
                    raise TimeoutError("Code execution timed out")

            except queue.Empty:
                if time.time() > deadline:
                    self.interrupt()
                    raise TimeoutError("Code execution timed out")
                continue

        return outputs

    def execute(self, code: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        执行代码并返回结果

        Args:
            code: 要执行的代码
            timeout: 可选的超时时间,覆盖默认值

        Returns:
            包含执行结果的字典
        """
        try:
            # 清除输出
            self.kernel_client.execute(code)
        except Exception as e:
            print(f"Error clearing output: {e}")
        return self._collect_outputs(timeout)

    def interrupt(self):
        """中断当前执行"""
        self.kernel_manager.interrupt_kernel()

    def shutdown(self):
        """关闭kernel"""
        try:
            # 先停止通道
            if self.kernel_client is not None:
                self.kernel_client.stop_channels()
            # 再关闭kernel
            if self.kernel_manager is not None:
                self.kernel_manager.shutdown_kernel(now=True)
        finally:
            # 清空引用
            self.kernel_client = None
            self.kernel_manager = None
