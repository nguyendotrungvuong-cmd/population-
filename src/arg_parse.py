import argparse


def arg_parse():
    parser = argparse.ArgumentParser(description="Tổng dân số tại năm")
    parser.add_argument("--country", default="vietnam")
    parser.add_argument(
        "--choice", choices=["new_json", "load_json"], default="new_json"
    )
    return parser.parse_args()
