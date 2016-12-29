import sys
import time
import string
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
        module_name = os.path.basename(event.src_path).rsplit('.py', maxsplit=1)[0]
        module_name = self.filter_module_letters(module_name)
        module_path = '{}.{}'.format(genscripts_dir, module_name)

        logging.debug('Module go load: {}'.format(module_path))
        try:
            if not self.is_module_loaded(module_path):
                module = importlib.import_module(module_path)
            else:
                module = importlib.reload(sys.modules[module_path])

        except SyntaxError as e:
            logging.error('Syntax error in {}: {}'.format(module_path, e))
            return
        except ImportError as e:
            logging.error('Import error for {}: {}'.format(module_path, e))
            return

        try:
            logging.info("{} {} {}".format(module_name, event.event_type, module))
            print(module.generate())
        except AttributeError:
            logging.warn('No `generate function in {}'.format(module_path))

    def filter_module_letters(self, path):
        return ''.join([c for c in path if c in string.ascii_letters])

    def is_module_loaded(self, module):
        return module in sys.modules.keys()


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
