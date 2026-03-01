import logging
import sys


def setup_logging(level: int = logging.INFO):
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configuración básica al stdout (consola)
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    external_loggers = [
        "httpx",
        "httpcore",
        "asyncio",
        "urllib3",
        "selector"
    ]

    for logger_name in external_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    root_logger = logging.getLogger("root")
    root_logger.info("Logging configurado: Librerías externas silenciadas.")