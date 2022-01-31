import csv
import os
from ast import literal_eval
from pathlib import Path
from typing import Iterable, Any, Tuple, Union

from wikipedia_extractor import Entity
from wikipedia_extractor.config import CONFIG
from wikipedia_extractor.utils import chunks
from wikipedia_extractor.writers import BaseWriter


class CsvWriter(BaseWriter):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.insert_batch_size = CONFIG["insert_batch_size"]

    def write(self, data: Iterable[Union[str, Tuple]], entity: Entity):
        os.makedirs(self.output_dir, exist_ok=True)
        path = Path(self.output_dir) / Path(f"{entity.value}.csv")

        with open(path, "w", newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=',')
            for records in chunks(map(CsvWriter._parse_record, data), self.insert_batch_size):
                csv_writer.writerows(records)

    @staticmethod
    def _parse_record(record: Union[str, Tuple]) -> Tuple:
        if isinstance(record, str):
            return literal_eval(record)
        elif isinstance(record, Tuple):
            return record
