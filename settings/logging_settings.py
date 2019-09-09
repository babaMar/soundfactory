import logging


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.propagate = 1  # propagate to parent
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s [%(levelname)s] %(message)s')
        console.setFormatter(formatter)
    return logger


viewlog = get_logger(name="view")
viewlog.setLevel(logging.INFO)
createlog = get_logger(name="create")
createlog.setLevel(logging.INFO)
