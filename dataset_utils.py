import collections
import pickle
import os
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords, wordnet as wn
from typing import Dict
from embeddings import get_best_sentence, get_data_from_articles

def create_stats_dict():
    hashmap = collections.defaultdict(int)
    article_ids = os.listdir("data/articles")
    all_text = ''

    for article_id in article_ids:
        all_text += ''.join( get_data_from_articles("data/articles/"+article_id))

    for token in all_text.split(' '):
        hashmap[token.lower()] += 1

    with open("dict.pkl", "wb") as f:
        pickle.dump(hashmap, f)

def get_data_from_sample(path: str) -> Dict:
    REPLACEMENTS =  [("(", ""), (")", ""),
                     ("[", ""), ("]", ""),
                     ("'", ""), ("\"", "")]
    with open(path, "r", encoding="utf8") as f:
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

def get_synonyms(word: str, pns: bool = False, max: int = 3):
    '''Returns a set of synonyms for a word
    @param word - Lowercase word to get synonyms for
    @param pns - True/False to include proper nouns (EX: panther -> Black Panthers)
    @param max - Maximum number of synonyms to return'''
    if pns:
        return set([w.name().replace("_", " ") for s in wn.synsets(word) for w in s.lemmas() if word != w.name()][0:max])
    return set([w.name().replace("_", " ") for s in wn.synsets(word) for w in s.lemmas() if word != w.name() and w.name() == w.name().lower()][0:max])

def expand_query(query: str):
    '''Returns an expanded query with synonyms for all non-stopwords'''
    STOPWORDS = set(stopwords.words('english'))
    new_query = ''
    for word in query.split():
        new_query += " " + word
        if word.lower() not in STOPWORDS:
            for synonym in get_synonyms(word.lower()):
                new_query += " " + synonym
    return new_query.strip()

def get_accuracy(data_dict):
    """
    `data_dict` is of the following type
        {'qa_idx': {'questions': List[questions], 'answers': List[answers]}}
    """
    for qa_index, qa_dict in tqdm(data_dict.items()):
        correct, count = 0, 0
        for question, answer in tqdm(zip(qa_dict['questions'], qa_dict['answers'])):
            response = get_best_sentence(question, [qa_index])
            if answer in response:
                correct += 1
            else:
                print('ID: ', qa_index, 'Question: ', question, 'Response: ', response, 'Answer: ', answer)
                print()
            count += 1
        acc = (correct/count)*100
        print(f"Accuracy on {qa_index}: {acc}")
    print('Overall Accuracy: ', acc)

def sample_check(PATH):
    df = pd.read_excel(PATH)
    questions, answers = list(df.question), list(df.answer_sentence)
    answers = list(map(str, answers))
    return questions, answers

sample_check("data/sample_check/sample.xlsx")
