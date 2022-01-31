import zlib
from itertools import chain, islice
from pathlib import Path
from typing import Iterable, List
from urllib.request import urlopen, Request

from tqdm import tqdm

from wikipedia_extractor.config import CONFIG


def chunks(iterable: Iterable, size: int) -> Iterable[List]:
    iterator = iter(iterable)
    for first in iterator:
        yield list(chain([first], islice(iterator, size - 1)))


def gzip_read_lines(url: str) -> Iterable[str]:
    file_name = Path(url).name
    response = urlopen(Request(url))
    file_size = int(response.headers.get('Content-Length'))
    read_block_size = CONFIG["read_block_size"]
    decompress_obj = zlib.decompressobj(zlib.MAX_WBITS | 32)

    prefix = ""
    with tqdm(unit='B', unit_scale=True, miniters=1, desc=f"{file_name}", total=file_size) as progress_bar:
        while progress_bar.n < file_size:
            compressed_data = response.read(read_block_size)
            decompressed_data = decompress_obj.decompress(compressed_data)
            content = prefix + decompressed_data.decode("utf-8", errors="replace")

            while decompress_obj.unused_data:
                unused_data = decompress_obj.unused_data
                decompress_obj = zlib.decompressobj(zlib.MAX_WBITS | 16)
                content += decompress_obj.decompress(unused_data).decode("utf-8", errors="replace")

            lines = content.split("\n")
            yield from lines[:-1]
            prefix = lines[-1]
            progress_bar.update(read_block_size)
        if prefix:
            yield prefix
