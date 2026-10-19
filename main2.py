import logging
import sys
from dotenv import load_dotenv

from src.api_client import fetch_data
from src.arg_parse import arg_parse
from src.config import get_api, get_url
from src.logging_setup import logging_setup
from src.parse_data import parse_data
from src.storage import save_json, load_json, save_csv


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
            logging.info("Đang lấy dữ liệu")

            data = fetch_data(API=API, URL=URL, country=args.country)

        else:
            logging.info("Đang load dữ liệu từ JSON cũ")

            data = load_json(country=args.country)

        # Cả hai mode đều phải kiểm tra dữ liệu
        logging.debug("Đang kiểm tra data contract")
        records = parse_data(data=data)

        logging.info("Data contract passed")

        # Chỉ lưu JSON mới sau khi validation thành công
        if args.choice == "new_json":
            save_json(country=args.country, data=data)
            logging.info("Đã lưu JSON")

        # Chỉ lưu CSV một lần
        save_csv(records=records, country=args.country)
        logging.info("Đã lưu CSV")

    except Exception as e:
        logging.error("Pipeline thất bại: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
