import os
import datetime
import queue
from collections import deque
import threading
import time


class ILog:

    def __init__(self, log_directory="logs", log_file_extension=".log"):
        self.log_queue = deque()

        self.stop_event = threading.Event()
        self._daemon = None

        self.start()
        self.log_file_extension = log_file_extension
        self.log_dir = os.path.join(os.getcwd(), log_directory)
        self._ensure_log_dir()

    def write(self, message):
        if self.stop_event.is_set():
            return
        self.log_queue.append(message)

    def stop(self, wait_for_completion):
        self.stop_event.set()
        if not wait_for_completion:
            self.log_queue.clear()
        self._daemon.join()

    def start(self):
        self.stop_event.clear()
        self._daemon = threading.Thread(target=self._write)
        self._daemon.start()

    def _write(self):
        while not self.stop_event.is_set():
            try:
                message = self.log_queue.popleft()
                # print(message)
                self._ensure_log_dir()
                # a+ creates new file if it doesn't exist
                with open(self._get_log_file_path(), "a+") as log_file:
                    log_file.write(message)
            except IndexError:
                time.sleep(1)
                pass
            except Exception as e:
                print(e)

    def _get_log_file_path(self):
        log_file = datetime.datetime.now().strftime("%Y_%m_%d") + self.log_file_extension
        return os.path.join(self.log_dir, log_file)

    def _ensure_log_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def __del__(self):
        self.stop(wait_for_completion=True)
