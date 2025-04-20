import functools
import logging
from typing import Final


# Caching, so that this doesn't get executed again when called, by accident.
@functools.cache
def setup() -> None:
    """Sets up the log configuration for the program."""
    all_logs_handler = logging.StreamHandler()
    colored_formatter = ColoredFormatter(datefmt="%Y-%m-%d %H:%M:%S")
    all_logs_handler.setFormatter(colored_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    root_logger.addHandler(all_logs_handler)


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        internal_formatter = self._get_level_formatter(record.levelno)
        return internal_formatter.format(record)

    # Colors taken from "colorama". I don't want to depend on it, though.
    # I'll be using a color, so I can easily see my log message by glancing at the output
    _BACKGROUND_GREEN = "\x1b[42m"
    _BACKGROUND_YELLOW = "\033[48;5;178m"
    _BACKGROUND_RED = "\x1b[41m"
    _BACKGROUND_RESET = "\x1b[49m"

    _LOG_LEVEL_COLOR: Final = {
        logging.DEBUG: "",
        logging.INFO: _BACKGROUND_GREEN,
        logging.WARNING: _BACKGROUND_YELLOW,
        logging.ERROR: _BACKGROUND_RED,
    }

    @classmethod
    @functools.cache
    def _get_level_formatter(cls, log_level: int) -> logging.Formatter:
        """Prepare a cached subformatter for particular message log level."""
        background_color = cls._LOG_LEVEL_COLOR.get(log_level, "")
        color_reset = cls._BACKGROUND_RESET if background_color else ""

        message_format = f"{background_color}--- %(asctime)s | %(levelname)s |{color_reset} %(message)s"

        return logging.Formatter(fmt=message_format)
