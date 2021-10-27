from dataclasses import dataclass
import spacy
from typing import List


@dataclass
class Tags:
    pos_tags: List[str]
    dep_tags: List[str]

def get_pos_tags(text: str):
    """
    Takes in a generic text and returns POS tags
    """
    sp = spacy.load('en_core_web_trf')
    text = sp(text)
    pos_tags, dep_tags = [], []
    for word in text:
        pos_tags.append(word.pos_)
    return Tags(pos_tags, dep_tags)
