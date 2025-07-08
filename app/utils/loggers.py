import logging
import builtins
import os
import sys

_original_print = builtins.print

def _log_print(*args, **kwargs):
    sep = kwargs.get('sep', ' ')
    message = sep.join(str(a) for a in args)
    logging.info(message)
    _original_print(*args, **kwargs)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        _original_print("KeyboardInterrupt")
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def setup_logging(log_file='logs/robocat.log'):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.captureWarnings(True)
    builtins.print = _log_print
    sys.excepthook = handle_exception
