import re
import time
import json
import subprocess
from enum import Enum
from pathlib import Path

from docker import DockerClient
from docker.errors import NotFound


class MTProtoProxy:
    _USER_CONFIG = Path(__file__).parent.parent / "config.json"

    class Color(str, Enum):
        RED = "\033[91m"
        BLUE = "\033[34m"
        GREEN = "\033[32m"

    def __init__(self) -> None:
        self.client = DockerClient()

        if not self._USER_CONFIG.exists():
            container_id = input(
                "Enter your tg_ws_proxy docker container id: "
            )

            try:
                self.client.containers.get(container_id)
            except NotFound:
                self._show_msg(
                    "Invalid tg_ws_proxy container id", 
                    self.Color.RED,
                )
                exit(1)
            
            with open(self._USER_CONFIG, mode="w") as file:
                data = {
                    "container_id": container_id,
                }
                file.write(json.dumps(data))
            
            self._show_msg(
                "Your container id will be saved in config.json "
                "(you can change it later)", 
                self.Color.BLUE,
            )

        else:
            with open(self._USER_CONFIG, mode="r") as file:
                data = json.loads(file.read())
                container_id = data["container_id"]

        self.container_id = container_id

    def connect(self) -> None:
        tg_ws_proxy_container = self.client.containers.get(self.container_id)        
        tg_ws_proxy_container.restart()
        
        self._show_msg(
            "Waiting for your container to restart...", 
            self.Color.BLUE,
        )
        time.sleep(3)

        logs = tg_ws_proxy_container.logs(tail=20).decode()
        matches = re.findall(
            r"(tg:\/\/proxy[?]server=[\d.]+&port=\d+&secret=\w+)", 
            logs
        )

        if matches:
            connection_url = matches[-1]
            subprocess.Popen(["xdg-open", connection_url])
            self._show_msg(
                "Proxy is connected! Check your Telegram.", 
                self.Color.GREEN,
            )

    @staticmethod
    def _show_msg(msg: str, color: Color) -> None:
        print(f"{color.value}{msg}\033[0m")
