#!/usr/bin/env python3


class LoggerError(Exception):
    """
    Namespace for errors the logger might raise
    """
    pass


class InvalidLevelError(LoggerError):
    """
    Exception to raise when the logger has been told to set itself to log an unknown level
    """
    pass


def start(name, level='INFO'):
    """

    :param name: The name that the root logger should be started under
    :param level:
    :return:
    """
    # Import logging to handle the majority of our logging processes
    import logging
    # Import colorlog to prettify our formatter.
    from colorlog import ColoredFormatter

    # Make a formatter
    formatter = ColoredFormatter(
        "%(bold_cyan)s%(asctime)-s%(reset)s%(log_color)s::%(module)s."
        "%(name)-14s::%(levelname)-10s%(reset)s%(blue)s%(message)-s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'bold_cyan',
            'INFO': 'bold_green',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red',
        }
    )
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    level = level.upper()
    if level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif level == 'INFO':
        logger.setLevel(logging.INFO)
    elif level == 'WARN' or level == 'WARNING':
        logger.setLevel(logging.WARN)
    elif level == 'FATAL' or level == 'ERROR' or level == 'SILENT':
        logger.setLevel(logging.FATAL)
    else:
        raise InvalidLevelError("The provided logging level doesn't exist")

    logger.info(f'Logger started for "%s"' % name)
    return logger
