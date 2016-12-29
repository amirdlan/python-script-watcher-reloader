import sys
import time
import logging
import importlib.util
import os.path
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler
import genscripts


genscripts_dir= 'genscripts'


class MyHandler(PatternMatchingEventHandler):
    def __init__(self, patterns, *args, **kwargs):
        super().__init__(patterns=patterns, *args, **kwargs)

    def on_created(self, event):
        self.handle_event(event)

    def on_modified(self, event):
        self.handle_event(event)

    def on_moved(self, event):
        self.handle_event(event)

    def handle_event(self, event):
        module_name = os.path.basename(event.src_path).rstrip('.py')
        module = importlib.import_module('{}.{}'.format(genscripts_dir, module_name))
        logging.debug('module {} {}'.format(module_name, module))
        print('gen', module.generate())


if __name__ == "__main__":
    sys.path.append('.{}'.format(genscripts_dir))
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    my_handler = MyHandler(patterns=['*.py'])
    observer = Observer()
    observer.schedule(my_handler,genscripts_dir)
    observer.start()
    try:
        logging.info("Running...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
