import os

import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util

from dataset_utils import get_data_from_articles

DATA_PATH = "data/articles"

def get_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def get_list_sentences(article_ids):
    all_data = {}
    for article_id in article_ids:
        all_data[article_id] = get_data_from_articles(os.path.join(DATA_PATH, str(article_id))+'.txt')
    return all_data


def compute_embedding_list_sentence(model, list_sentences):
    list_sentences_embedding = model.encode(list_sentences, convert_to_tensor=True)
    return list_sentences_embedding


def get_best_sentence(query, article_ids):
    all_sentences_dict = get_list_sentences(article_ids)

    model = get_model()
    original_query_embedding = model.encode(query)
    candidate_sentences_data = {}

    for article_id, article_id_sentences in all_sentences_dict.items():
        query_embedding = torch.tensor(np.array([len(article_id_sentences)*[original_query_embedding]]))
        query_embedding = query_embedding.squeeze(0)

        article_id_embedding = compute_embedding_list_sentence(model, article_id_sentences)
        article_id_cosine_score = util.pytorch_cos_sim(query_embedding, article_id_embedding)
        candidate_sentences_data[article_id] = torch.max(article_id_cosine_score[0], dim=0)

    best_score = 0
    best_sentence = ""
    for article_id, (max_score, sentence_id) in candidate_sentences_data.items():
        if max_score > best_score:
            best_score = max_score
            best_sentence = all_sentences_dict[article_id][sentence_id]
    return best_sentence



