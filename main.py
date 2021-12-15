from tqdm import tqdm
from indexer import search
import pickle
from dataset_utils import get_accuracy, get_data_from_sample, sample_check
from embeddings import get_best_sentence
from _filter import filter_query_retrieval, filter_query

SAMPLE_DATA_PATH = "data/qa_data.txt"
SAMPLE_DATA_VALIDATION = "data/sample_check/sample.xlsx"

if __name__ == '__main__':
    questions, answers = sample_check(SAMPLE_DATA_VALIDATION)
    correct = 0
    for sample_question, sample_answer in tqdm(zip(questions, answers)):
        filtered_query = filter_query_retrieval(sample_question)
        # retrieved_article_text = search(filtered_query, highlight=True)
        # response = filter_query(get_best_sentence(sample_question, retrieved_article_text))
        retrieved_article_ids = search(filtered_query)
        response = filter_query(get_best_sentence(sample_question, retrieved_article_ids))
        sample_answer = filter_query(sample_answer)

        if str(sample_answer) in response:
            correct += 1
        else:
            print('\nResponse: ', response, '\nGround Truth: ', sample_answer, "\n")
    print('Accuracy: ', correct/len(questions))

        #  print('Response: ', response, 'Ground Truth: ', sample_answer)

    #  query = "What was the capital of the Safavid Dynasty ?"
#      key_word = filter_query_retrieval(query)
    #  article_ids = search(key_word)
    #  sample_data_dict = get_data_from_sample(SAMPLE_DATA_PATH)
#      get_accuracy(sample_data_dict)
