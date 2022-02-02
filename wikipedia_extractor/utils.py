import bz2
import gzip
import os.path
import urllib.parse
import warnings
import zlib
from itertools import chain, islice
from pathlib import Path
from sqlite3 import Cursor
from typing import Iterable, List
from urllib.request import urlopen, Request

from tqdm import tqdm

from wikipedia_extractor import Entity
from wikipedia_extractor.config import CONFIG

READ_BLOCK_SIZE = CONFIG["read_block_size"]


def chunks(iterable: Iterable, size: int) -> Iterable[List]:
    iterator = iter(iterable)
    for first in iterator:
        yield list(chain([first], islice(iterator, size - 1)))


def read_compressed(path: str, filename: str) -> Iterable[str]:
    path = str(Path(path).absolute() / filename)
    try:
        yield from read_compressed_from_file(path)
    except FileNotFoundError:
        warnings.warn(f"File not found: {path}, switching to streaming...")
        url = urllib.parse.urljoin(CONFIG["base_url"], filename)
        yield from read_compressed_from_url(url)


def read_compressed_from_file(path: str) -> Iterable[str]:
    file_size = os.path.getsize(path)

    prefix = ""
    with tqdm(unit='B', unit_scale=True, miniters=1, desc=f"{path}", total=file_size) as progress_bar:
        with _open(path) as file:
            while progress_bar.n < file_size:
                data = file.read(READ_BLOCK_SIZE)
                content = prefix + data.decode('utf8', errors='replace')
                lines = content.split("\n")
                yield from lines[:-1]
                prefix = lines[-1]
                progress_bar.update(READ_BLOCK_SIZE)


def read_compressed_from_url(url: str) -> Iterable[str]:
    response = urlopen(Request(url))
    file_size = int(response.headers.get('Content-Length'))

    decompressor = _get_decompressor(url)
    prefix = ""
    with tqdm(unit='B', unit_scale=True, miniters=1, desc=f"{url}", total=file_size) as progress_bar:
        while progress_bar.n < file_size:
            compressed_data = response.read(READ_BLOCK_SIZE)
            decompressed_data = decompressor.decompress(compressed_data)
            content = prefix + decompressed_data.decode("utf-8", errors="replace")

            while decompressor.unused_data:
                unused_data = decompressor.unused_data
                decompressor = _get_decompressor(url)
                content += decompressor.decompress(unused_data).decode("utf-8", errors="replace")

            lines = content.split("\n")
            yield from lines[:-1]
            prefix = lines[-1]
            progress_bar.update(READ_BLOCK_SIZE)
        if prefix:
            yield prefix


def _get_decompressor(filename: str):
    extension = Path(filename).suffix
    if extension == ".gz":
        return zlib.decompressobj(zlib.MAX_WBITS | 32)
    elif extension == ".bz2":
        return bz2.BZ2Decompressor()
    else:
        raise ValueError(f"Invalid extension: {extension}")


def _open(path: str):
    extension = Path(path).suffix
    if extension == ".gz":
        return gzip.open(path, "rb")
    elif extension == ".bz2":
        return bz2.BZ2File(path, "rb")
    else:
        raise ValueError(f"Invalid extension: {extension}")


def get_count(cursor: Cursor, entity: Entity) -> int:
    cursor.execute(f"SELECT COUNT(*) FROM {entity.value}")
    return int(cursor.fetchone()[0])
