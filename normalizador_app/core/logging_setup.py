import logging


def setup_logging() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("normalizador_errors.log"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger("normalizador")
