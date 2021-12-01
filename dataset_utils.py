import sys
from dataclasses import dataclass
from tqdm import tqdm
from typing import List, Dict


def get_data_from_articles(path: str) -> List:
    with open(path, "r") as f:
        data = f.read()
    data = data.split(".")
    return data

def get_data_from_sample(path: str) -> Dict:
    replacements =  [("(", ""), (")", ""),
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
                for k, v in replacements:
                    clean_question = clean_question.replace(k, v)
                questions.append(clean_question.strip())
            else:
                clean_answer = example[idx]
                for k, v in replacements:
                    clean_answer = clean_answer.replace(k, v)
                answers.append(clean_answer.strip())
        qa_dict[qa_index] = {'questions': questions, 'answers': answers}
    return qa_dict
