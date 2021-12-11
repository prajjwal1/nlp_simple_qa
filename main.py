from tqdm import tqdm
#  from embeddings import get_best_sentence
#  from dataset_utils import get_data_from_sample, expand_query
from indexer import search
import pickle

SAMPLE_DATA_PATH = "data/qa_data.txt"

def get_accuracy(data_dict):
    """
    `data_dict` is of the following type
        {'qa_idx': {'questions': List[questions], 'answers': List[answers]}}
    """
    for qa_index, qa_dict in tqdm(data_dict.items()):
        correct, count = 0, 0
        for question, answer in tqdm(zip(qa_dict['questions'], qa_dict['answers'])):
            response = get_best_sentence(question, [qa_index])
            print('Question: ', question, 'Response: ', response, 'Answer: ', answer)
            print()
            if answer in response:
                correct += 1
            count += 1
        acc = (correct/count)*100
        print(f"Accuracy on {qa_index}: {acc}")
    print('Overall Accuracy: ', acc)

def filter_query(query):
    words_to_remove = ["how", "when", "what", "?", "was", "the", "of", "the"]
    query = ' '.join([x for x in query.split() if x not in words_to_remove])
    return query

def standardize_query(query):
    query = query.lower()
    return query

def filter_query_retrieval(query):
    query = standardize_query(query)

    with open("dict.pkl", "rb") as f:
        freq_stats = pickle.load(f)
    freqs_each_token = []
    query = filter_query(query)

    for val in query.split():
        freqs_each_token.append(freq_stats[val])

    query_list = query.split()
    return query_list[freqs_each_token.index(min(freqs_each_token))]


if __name__ == '__main__':
    # Example of how to expand query
    query = "What was the capital of the Safavid Dynasty ?"
    key_word = filter_query_retrieval(query)

    article_ids = search(key_word)
    print(article_ids)
    #  print(expand_query('Giant Wholesome Penguins Attack Tigers on the Antarctic Ice Shelf'))
    #  sample_data_dict = get_data_from_sample(SAMPLE_DATA_PATH)
    #  get_accuracy(sample_data_dict)
