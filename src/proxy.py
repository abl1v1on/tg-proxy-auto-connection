import re
import time
import subprocess
from enum import Enum
from pathlib import Path

from docker import DockerClient
from docker.errors import NotFound


class MTProtoProxy:
    class Color(str, Enum):
        RED = "\033[91m"
        BLUE = "\033[34m"
        GREEN = "\033[32m"

    def __init__(
        self, 
        telegram_bin_path: Path, 
        tg_ws_proxy_container_id: str,
    ) -> None:
        if not telegram_bin_path.exists():
            self._show_msg(
                "Invalid path to telegram bin file", 
                self.Color.RED,
            )
            exit(1)

        self.tg_bin_path = telegram_bin_path
        self.tg_ws_proxy_container_id = tg_ws_proxy_container_id

    def connect(self) -> None:
        client = DockerClient()
        
        try:
            tg_ws_proxy_container = client.containers.get(
                self.tg_ws_proxy_container_id
            )
        except NotFound:
            self._show_msg(
                "Invalid tg_ws_proxy container id", 
                self.Color.RED,
            )
            exit(1)
        
        tg_ws_proxy_container.restart()
        self._show_msg(
            "Waiting for your container to restart...", 
            self.Color.BLUE,
        )
        time.sleep(2)

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
