from __future__ import annotations

import threading
import socket
import json

class Connection():
    queue_funcs: list[str] = []

    def __init__(self, c: socket.socket):
        self.c = c
        self.func_queue = {}
        threading.Thread(target=self.__main__, daemon=True).start()

    def __main__(self):
        data = ""
        try:
            while True:
                data += self.c.recv(1024).decode()
                if "§" in data:
                    data = data.split("§", 1)
                    packet = json.loads(data[0])
                    data = data[1]
                    func: function = getattr(self, packet["type"])
                    if packet["type"] in self.queue_funcs:
                        self.func_queue.update({packet["type"]: lambda: func(packet)})
                    else:
                        func(packet)
                
        except ConnectionResetError:
            self.__main_error__()

    def __main_error__(self):
        pass

    def run_queue(self):
        for func in self.func_queue.values():
            func()