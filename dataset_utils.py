from dataclasses import dataclass
from datasets import load_dataset
import spacy
from spacy.lang.en import English
from tqdm import tqdm
from typing import List

@dataclass
class TokenizedComponents:
    tokenized_answers: List[int]
    tokenized_context: List[int]
    tokenized_titles: List[int]

def get_data(dataset_name, split, tokenization=False, return_raw_dataset=False):
    """
    Returns the dataset in a tokenized format
    """
    dataset = load_dataset(dataset_name, split=split)
    if tokenization:
        all_answers, all_context, all_titles  = [], [], []
        for idx in range(len(dataset)):
            all_answers.append(dataset[idx]['answers'])
            all_context.append(dataset[idx]['context'])
            all_titles.append(dataset[idx]['title'])

        nlp = English()
        tokenizer = nlp.tokenizer
        all_answers_tokenized, all_context_tokenized, all_titles_tokenized = [], [], []
        for val in tqdm(all_answers, desc="Tokenizing Answers"):
            all_answers_tokenized.append(tokenizer(val['text'][0]))
        for val in tqdm(all_context, desc="Tokenizing Context"):
            all_context_tokenized.append(tokenizer(val))
        for val in tqdm(all_titles, desc="Tokenizing Titles"):
            all_titles_tokenized.append(tokenizer(val))

        return TokenizedComponents(
            all_answers_tokenized,
            all_context_tokenized,
            all_titles_tokenized
        )
    if return_raw_dataset:
        return dataset


def Lemmatizer(sentence):
    nlp = spacy.load('en_core_web_trf', disable = ['parser', 'tagger', 'ner'])
    doc = nlp(sentence)
    lemmatized_tokens = [token.lemma_ for token in doc]
    return lemmatized_tokens
