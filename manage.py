import sys
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.subprocess = None
        self.start_script()

    def start_script(self):
        if self.subprocess:
            self.subprocess.terminate()  # Terminate the existing subprocess

        print("Starting __main__.py...")
        self.subprocess = subprocess.Popen([sys.executable, "__main__.py"])

    def on_modified(self, event):
        if (
            event.src_path.endswith("/.git/")
            or event.src_path.endswith("/.githib/")
            or event.src_path.endswith("/.mypy_cache/")
            or event.src_path.endswith("/__pycache__/")
            or event.src_path.endswith("/venv/")
        ):
            pass
        else:
            if event.src_path.endswith("__main__.py"):
                print("Restarting __main__.py...")
                self.start_script()
                print("Script restarted.")


if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()
    path_to_watch = "."  # Change this to the directory you want to monitor
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)  # Sleep to prevent busy-waiting
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
