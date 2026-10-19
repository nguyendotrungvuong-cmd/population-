import csv
import json
from pathlib import Path
from src.logging_setup import logging_setup
import pandas as pd
import logging

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)
raw_json = DATA / "raw"
raw_json.mkdir(parents=True, exist_ok=True)
staging = DATA / "staging"
staging.mkdir(parents=True, exist_ok=True)
final = DATA / "final"
final.mkdir(parents=True, exist_ok=True)
list_json = []
logging_setup()


def save_json(country, data):
    file_path = raw_json / f"{country}.json"
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
    return file_path


def load_json(country):

    file_path = raw_json / f"{country}.json"
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception:
        logging.error(f"{country}.json chưa tồn tại, vui lòng tạo mới bằng new_json")
        raise
    else:
        return data


def save_csv(records, country):
    columns = list(records[0].keys())
    file_path = staging / f"{country}.csv"
    with file_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)
    return file_path


def csv_staging(country):
    file_path = Path(staging)
    df = pd.read_csv(file_path / f"{country}.csv")
    df["country"] = f"{country}"
    df.to_csv(final / f"{country}.csv")
    # còn thêm cách hàm kiểm tra, đây là demo.
