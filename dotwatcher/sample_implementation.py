#!/usr/bin/env python3
from shutil import rmtree
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TARGET_PATH_TO_MONITOR = Path.home() / ".pki"
PARENT_DIR = TARGET_PATH_TO_MONITOR.parent

class ContinuousHandler(FileSystemEventHandler):
    def __init__(self, target_full_path: Path):
        self.target_full_path = target_full_path

    def on_created(self, event):
        # TODO logging instead of print
        print(f'event {event}')
        if event.src_path == self.target_full_path.as_posix():
            print(f"Path '{self.target_full_path}' created at {time.asctime()}. Removing")
            rmtree(self.target_full_path, ignore_errors=True)


if __name__ == "__main__":
    if not PARENT_DIR.is_dir():
        print(f"Error: Parent directory '{PARENT_DIR}' does not exist. Cannot monitor.")
        exit(1)

    observer = Observer()
    event_handler = ContinuousHandler(TARGET_PATH_TO_MONITOR)
    observer.schedule(event_handler, PARENT_DIR, recursive=False)
    observer.start()
    print(f"Continuously monitoring '{PARENT_DIR}' for creation of '{TARGET_PATH_TO_MONITOR}'. Press Ctrl+C to stop.")

    try:
        observer.join()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, stopping observer.")
        observer.stop()
    finally:
        # TODO remove comment, add self-explanatory function
        # Ensure the observer thread is cleaned up properly.
        if observer.is_alive():
            observer.join()
        print("Monitoring stopped.")
