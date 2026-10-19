import logging
import os
from google.cloud import bigquery
from dotenv import load_dotenv
from src.api_client import fetch_data
from src.arg_parse import arg_parse
from src.bq_loader import load_to_bigquery
from src.config import *
from src.logging_setup import logging_setup
from src.parse_data import parse_data
from src.storage import *

import pandas as pd


def main():
    load_dotenv()
    args = arg_parse()
    API = get_api()
    URL = get_url()
    logging_setup()
    print(f"Country: {args.country}")
    print(f"Mode: {args.choice}")
    try:
        if args.choice == "new_json":
            logging.info(f"{args.choice}")
            logging.info("Đang lấy dữ liệu")
            data = fetch_data(API=API, URL=URL, country=args.country)
            logging.debug("Đang kiểm tra data contract")
            records = parse_data(data)
            save_json(country=args.country, data=data)

            save_csv(records=records, country=args.country)
            logging.info("Đã lưu CSV")
        else:
            logging.info(f"{args.choice}")
            logging.info("Đang load dữ liệu từ json cũ")
            data = load_json(country=args.country)
            logging.info("Đã load thành công")
            logging.info("Đang tiến hành phân tích dữ liệu")

        records = parse_data(data=data)
        logging.info("Đã pass")
        save_csv(records=records, country=args.country)
        logging.info("Đã lưu CSV vào staging")
        csv_staging(country=args.country)
        logging.info("Đã xử lý và lưu vào final")
        load_to_bigquery(country=args.country)
        logging.info("Đã load lên bigquery thành công")
    except :
        logging.error("Thất bại:")
        raise
    else:
        logging.info("Pipeline đã xử lý thành công!")


if __name__ == "__main__":
    main()
