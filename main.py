import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler


class MyHandler(PatternMatchingEventHandler):
    def __init__(self, pattern, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_created(self, event):
        self.handle_event(event)

    def on_modified(self, event):
        self.handle_event(event)

    def on_moved(self, event):
        self.handle_event(event)

    def handle_event(self, event):
        print("HI!!!!", event.src_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging_handler = LoggingEventHandler()
    my_handler = MyHandler('*.py')
    observer = Observer()
    directory = 'genscripts'
    observer.schedule(logging_handler, directory)
    observer.schedule(my_handler, directory)
    observer.start()
    try:
        print("Running...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
