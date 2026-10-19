from pathlib import Path
from google.cloud import bigquery
from src.logging_setup import logging_setup
import logging
logging_setup()


def load_to_bigquery(country):
    client = bigquery.Client()

    project_id = client.project
    dataset_id = "population_lab"
    table_id = f"{country}"

    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    file_path = Path("data/final") / f"{country}.csv"

    job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with open(file_path, "rb") as file:
        job = client.load_table_from_file(
            file,
            table_ref,
            job_config=job_config,
            location="US",
        )

    job.result()

    logging.info(f"Load thành công: {file_path} → {table_ref}")