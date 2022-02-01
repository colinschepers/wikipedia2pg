import bz2
import zlib
from itertools import chain, islice
from pathlib import Path
from sqlite3 import Cursor
from typing import Iterable, List
from urllib.request import urlopen, Request

from tqdm import tqdm

from wikipedia_extractor import Entity
from wikipedia_extractor.config import CONFIG


def chunks(iterable: Iterable, size: int) -> Iterable[List]:
    iterator = iter(iterable)
    for first in iterator:
        yield list(chain([first], islice(iterator, size - 1)))


def read_compressed(url: str) -> Iterable[str]:
    file_name = Path(url).name
    response = urlopen(Request(url))
    file_size = int(response.headers.get('Content-Length'))
    read_block_size = CONFIG["read_block_size"]
    decompressor = get_decompressor(url)

    prefix = ""
    with tqdm(unit='B', unit_scale=True, miniters=1, desc=f"{file_name}", total=file_size) as progress_bar:
        while progress_bar.n < file_size:
            compressed_data = response.read(read_block_size)
            decompressed_data = decompressor.decompress(compressed_data)
            content = prefix + decompressed_data.decode("utf-8", errors="replace")

            while decompressor.unused_data:
                unused_data = decompressor.unused_data
                decompressor = get_decompressor(url)
                content += decompressor.decompress(unused_data).decode("utf-8", errors="replace")

            lines = content.split("\n")
            yield from lines[:-1]
            prefix = lines[-1]
            progress_bar.update(read_block_size)
        if prefix:
            yield prefix


def get_decompressor(url: str):
    extension = Path(url).suffix
    if extension == ".gz":
        return zlib.decompressobj(zlib.MAX_WBITS | 16)
    elif extension == ".bz2":
        return bz2.BZ2Decompressor()
    else:
        raise ValueError(f"Invalid extension: {extension}")


def get_count(cursor: Cursor, entity: Entity) -> int:
    cursor.execute(f"SELECT COUNT(*) FROM {entity.value}")
    return int(cursor.fetchone()[0])
