from dataclasses import dataclass
from tqdm import tqdm
from typing import List


def get_data_from_articles(path: str) -> List:
    with open(path, "r") as f:
        data = f.read()
    data = data.split(".")
    return data

