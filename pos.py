import spacy


def get_pos_tags(text: str):
    """
    Takes in a generic text and returns POS tags
    """
    sp = spacy.load('en_core_web_trf')
    text = sp(text)
    pos_tags = []
    for word in text:
        pos_tags.append(word.pos_)
    return pos_tags
