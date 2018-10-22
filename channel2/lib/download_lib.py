from typing import NamedTuple, Text
from urllib import parse

import requests

FileData = NamedTuple('File', [
    ('bytes', bytes),
    ('extension', Text),
])


def download_file(url: Text) -> FileData:
    extension = parse.urlparse(url).path.split('.')[-1]
    cover_bytes = requests.get(url).content
    return FileData(cover_bytes, extension)
