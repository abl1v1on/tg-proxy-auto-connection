# MTProto Auto Connection
Скрипт позволяет быстро и удобно настраивать **MTProto** прокси для телеграма (с использованием Docker образа **tg-ws-proxy**)
> **⚠️ Warning:** Скрипт предназначен только для UNIX-подобных систем.

## Установка
Создайте Docker контейнер `tg-ws-proxy` по гайду от разработчика https://github.com/Flowseal/tg-ws-proxy/blob/main/docs/README.docker.md

После создания Docker контейнера склонируйте этот репозиторий:
~~~bash
git clone "https://github.com/abl1v1on/tg-proxy-auto-connection.git"
cd tg-proxy-auto-connection
~~~

Установите зависимости:
~~~bash
python3 -m venv .venv

# pip
pip install -r requirements.txt

# uv
uv sync
~~~

Сделайте файл `tg-proxy.sh` исполняемым и создайте симлинк:
~~~bash
sudo chmod +x tg-proxy.sh
ln -s /path/to/tg-proxy-auto-connection/tg-proxy.sh /usr/local/bin/tg-proxy
~~~

Перед запуском скрипта необходимо добавить пользователя в группу docker (или, пропустив этот шаг, запускать скрипт с sudo):
~~~
sudo usermod -aG docker $USER
sudo reboot

# После перезагрузки!!
newgrp docker
~~~

Теперь вы можете вызывать `tg-proxy` из любого места:
~~~bash
tg-proxy
~~~

При первом запуске необходимо ввести id контейнера `tg-ws-proxy`:
~~~bash
sudo docker ps

        ⬇
> 81ec444b4cf5 lordarrin/tg-ws-proxy:latest "/usr/bin/tini -- /e…" 9 days ago Up 5 minutes 0.0.0.0:1443->1443/tcp, [::]:1443->1443/tcp tg-ws-proxy
~~~

> 🚨 Если после запуска вы не видите сообщение **"Proxy is connected! Check your Telegram."** - попробуйте увеличить `time.sleep(n)` в файлe `src/proxy.py`
