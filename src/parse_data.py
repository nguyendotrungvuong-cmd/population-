import logging


def parse_data(data):
    try:
        if data == []:
            raise ValueError("Data rỗng hoặc tên quốc gia không phù hợp")

        if not isinstance(data, dict):
            raise TypeError("Data phải là dict")

        records = data.get("historical_population")

        if not isinstance(records, list):
            raise TypeError("Records phải là list")

        if not records:
            raise ValueError("historical_population rỗng")

        expected_columns = set(records[0].keys())

        for index, record in enumerate(records, start=1):
            if not isinstance(record, dict):
                raise TypeError(f"Record {index} phải là dict")

            wrong = expected_columns - set(record.keys())

            if wrong:
                raise ValueError(f"Record {index} thiếu các cột: {wrong}")

    except Exception:
        logging.exception("Lỗi khi parse dữ liệu")
        raise

    else:
        return records
