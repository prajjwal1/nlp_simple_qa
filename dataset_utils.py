import sys
from dataclasses import dataclass
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from typing import List, Dict


def get_data_from_articles(path: str) -> List:
    with open(path, "r") as f:
        data = f.read()
    data = data.split(".")
    return data

def get_data_from_sample(path: str) -> Dict:
    REPLACEMENTS =  [("(", ""), (")", ""),
                     ("[", ""), ("]", ""),
                     ("'", ""), ("\"", "")]
    with open(path, "r") as f:
        data = f.read()
    data = data.split("\n")
    examples = []
    for val in data:
        examples.append(val.split(", "))
    qa_dict = {}
    for example in examples:
        try:
            qa_index = int(example[0].replace("[", ""))
        except ValueError:
            print(example[0])
        questions, answers = [], []
        for idx in range(1, len(example)):
            if idx%2 != 0:
                clean_question = example[idx]
                for k, v in REPLACEMENTS:
                    clean_question = clean_question.replace(k, v)
                questions.append(clean_question.strip())
            else:
                clean_answer = example[idx]
                for k, v in REPLACEMENTS:
                    clean_answer = clean_answer.replace(k, v)
                answers.append(clean_answer.strip())
        qa_dict[qa_index] = {'questions': questions, 'answers': answers}
    return qa_dict

def get_synonyms(word: str, pns = False, max: int = 3):
    '''Gets synonyms for a word
    @param word - Lowercase word to get synonyms for
    @param pns - True/False to include proper nouns (EX: panther -> Black Panthers)
    @param max - Maximum number of synonyms to return'''
    if pns:
        return set([w.name().replace("_", " ") for s in wn.synsets(word) for w in s.lemmas() if word != w.name()][0:max])
    return set([w.name().replace("_", " ") for s in wn.synsets(word) for w in s.lemmas() if word != w.name() and w.name() == w.name().lower()][0:max])

def expand_query(query: str):
    '''Expands a query to include synonyms for non stop words'''
    STOPWORDS = set(stopwords.words('english'))
    new_query = ''
    for word in query.split():
        new_query += " " + word
        if word.lower() not in STOPWORDS:
            for synonym in get_synonyms(word.lower()):
                new_query += " " + synonym
    return new_query.strip()