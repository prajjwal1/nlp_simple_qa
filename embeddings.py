import os
from typing import List
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util

DATA_PATH = "data/articles"

def get_model() -> SentenceTransformer:
    return SentenceTransformer("all-MiniLM-L6-v2", device="cuda" if torch.cuda.is_available() else "cpu")

def get_data_from_articles(path: str) -> List:
    with open(path, "r", encoding="utf8") as f:
        data = f.read()
    return data.split(".")

def get_list_sentences(article_ids):
    all_data = {}
    for article_id in article_ids:
        all_data[article_id] = get_data_from_articles(os.path.join(DATA_PATH, str(article_id))+'.txt')
    return all_data

def compute_embedding_list_sentence(model, list_sentences):
    return model.encode(list_sentences, convert_to_tensor=True)

def get_best_sentence(query, article_ids):
    all_sentences_dict = get_list_sentences(article_ids)
    # all_sentences_dict = get_list_sentences([k for k, v in article_text.items()]) # Whole Doc
    # all_sentences_dict = {k: v['text'] for k, v in article_text.items()} # Search Highlighted Sentences

    model = get_model()
    original_query_embedding = model.encode(query, convert_to_tensor=True)
    candidate_sentences_scores, candidate_sentences = [], []
    all_article_ids = []

    for article_id, article_id_sentences in all_sentences_dict.items():
        input_sentences = [query]
        input_sentences.extend(article_id_sentences)

        query_embedding = original_query_embedding.repeat(len(article_id_sentences), 1)
        corpus_embedding = compute_embedding_list_sentence(model, article_id_sentences)

        cos_scores = util.semantic_search(query_embedding, corpus_embedding, top_k=1)
        candidate_sentences_scores.append(cos_scores[0][0]['score'])
        candidate_sentences.append(article_id_sentences[cos_scores[0][0]['corpus_id']])
        all_article_ids.append(article_id)

    best_idx = np.argmax(candidate_sentences_scores)
    return candidate_sentences[best_idx], all_article_ids[best_idx]

    # #Paraphrase mining
    # paraphrases = util.paraphrase_mining(model, input_sentences, batch_size=128)
    # best_sentence, best_score = [], []
    # for score, sentence_i, sentence_j in paraphrases:
    #     if (sentence_i == 0):
    #         best_sentence.append(article_id_sentences[sentence_j-1])
    #         best_score.append(score)
    #     elif sentence_j == 0:
    #         best_sentence.append(article_id_sentences[sentence_i-1])
    #         best_score.append(score)
    # return best_sentence[np.argmax(best_score)]

    # #Vanilla Cosine similarity
    #  query_embedding = original_query_embedding.repeat(len(article_id_sentences), 1)
    #  article_id_embedding = compute_embedding_list_sentence(model, article_id_sentences)
    #  article_id_cosine_score = util.pytorch_cos_sim(query_embedding, article_id_embedding)
    #  candidate_sentences_data[article_id] = torch.max(article_id_cosine_score[0], dim=0)

    # #best_score = 0
    # best_sentence = ""
    # for article_id, (max_score, sentence_id) in candidate_sentences_data.items():
    #     if max_score > best_score:
    #         best_score = max_score
    #         best_sentence = all_sentences_dict[article_id][sentence_id]
    # return best_sentence
