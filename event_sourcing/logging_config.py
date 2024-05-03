import logging
import sys


class CustomFormatter(logging.Formatter):
    blue = "\033[34;21m"
    purple = "\033[35m"
    yellow = "\033[33;21m"
    red = "\033[31;21m"
    bold_red = "\033[31;1m"
    reset = "\033[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: purple + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logging(debug=True, logging_level=logging.INFO):
    if debug:

        handler_sh = logging.StreamHandler(sys.stdout)
        handler_sh.setFormatter(CustomFormatter())

        logging.basicConfig(
            level=logging_level,
            handlers=[handler_sh]
        )
    else:
        logging.basicConfig(
            filename="main.log",
            level=logging_level,
        )
    mode = "dev" if debug else "production"
    logging.getLogger(__name__).info(f"lancement du programme en mode [{mode}]")
    # change le niveau de log du logger kafka
    logger_kafka = logging.getLogger("kafka")
    logger_kafka.setLevel(logging.WARN)
