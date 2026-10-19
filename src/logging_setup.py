import logging
from pathlib import Path


def logging_setup():
    ROOT = Path(__file__).resolve().parent.parent
    LOG = ROOT / "log"
    LOG.mkdir(parents=True, exist_ok=True)
    a = logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(message)s",
        level=logging.DEBUG,
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG / "pipeline.log", mode="a", encoding="utf-8"),
        ],
        force=True,
    )
    return logging.getLogger(__name__)
