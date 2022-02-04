import bz2
import gzip
import os.path
import urllib.parse
import warnings
import zlib
from itertools import chain, islice
from pathlib import Path
from sqlite3 import Cursor
from typing import Iterable, List, BinaryIO
from urllib.request import urlopen, Request, urlretrieve

from tqdm import tqdm

from wikipedia2pg import Entity
from wikipedia2pg.config import CONFIG

READ_BLOCK_SIZE = CONFIG["read_block_size"]


def chunks(iterable: Iterable, size: int) -> Iterable[List]:
    iterator = iter(iterable)
    for first in iterator:
        yield list(chain([first], islice(iterator, size - 1)))


def read_compressed(path: str, filename: str) -> Iterable[str]:
    path = Path(path).absolute() / filename

    if not path.exists():
        url = urllib.parse.urljoin(CONFIG["base_url"], filename)
        _download_dump(url, path)

    file_size = os.path.getsize(path)
    with tqdm(unit='B', unit_scale=True, miniters=1, desc=f"Processing {path}", total=file_size) as progress_bar:
        with open(path, "rb") as file, _open_zip(file) as zip_file:
            for line in zip_file:
                yield line.decode('utf8', errors='replace')
                progress_bar.update(file.tell() - progress_bar.n)


def _download_dump(url: str, path: Path):
    def tqdm_hook(t):
        last_b = [0]

        def inner(transfered_blocks=1, block_size=1, total_size=None):
            if total_size is not None:
                t.total = total_size
            t.update((transfered_blocks - last_b[0]) * block_size)
            last_b[0] = transfered_blocks

        return inner

    os.makedirs(path.parent, exist_ok=True)
    with tqdm(unit='B', unit_scale=True, miniters=1, desc=f"Downloading {path.name}") as progress_bar:
        urlretrieve(url, filename=str(path), reporthook=tqdm_hook(progress_bar), data=None)


def _open_zip(file: BinaryIO):
    extension = Path(file.name).suffix
    if extension == ".gz":
        return gzip.open(file, "rb")
    elif extension == ".bz2":
        return bz2.BZ2File(file, "rb")
    else:
        raise ValueError(f"Invalid extension: {extension}")


def get_count(cursor: Cursor, entity: Entity) -> int:
    cursor.execute(f"SELECT COUNT(*) FROM {entity.value}")
    return int(cursor.fetchone()[0])
