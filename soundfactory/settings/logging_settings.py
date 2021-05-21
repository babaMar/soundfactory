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

plotterlog = get_logger(name="plotter")
plotterlog.setLevel(logging.INFO)

playlog = get_logger(name="play")
playlog.setLevel(logging.INFO)

signal_log = get_logger(name="signal")
signal_log.setLevel(logging.DEBUG)

helperlog = get_logger(name="helper")
helperlog.setLevel(logging.INFO)
