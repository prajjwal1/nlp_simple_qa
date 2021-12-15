from tqdm import tqdm
from indexer import search
from dataset_utils import expand_query, get_accuracy, get_data_from_sample, get_lemmas, get_pos_tags, remove_stopwords, sample_check
from embeddings import get_best_sentence
import fire
from _filter import filter_query_retrieval, filter_query

SAMPLE_DATA_PATH = "data/qa_data.txt"
SAMPLE_DATA_VALIDATION = "data/sample_check/sample.xlsx"

def run_inference_sample():
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

def run_task_1():
    questions = [q.lower().replace('"', '').replace('?', '').replace('.', '').replace('“', '').replace('”', '')
        .replace('!', '').replace('-', '').replace('—', '').replace(';', '').replace(',', '').replace('(', '')
        .replace(')', '').replace('/', '').replace('\\', '').replace('\n', '').replace('\t', '').replace('\r', '')
        for q_list in sample_check(SAMPLE_DATA_VALIDATION) for q in q_list]
    i = 1
    for question in questions:
        print(f'Question #{i}:', question)
        question_filtered = remove_stopwords(question)
        print('POS Tagged:', get_pos_tags(question))
        print('Word Filter:', question_filtered)
        print('Lemmatized:', get_lemmas(question_filtered))
        print('Expanded Query:', expand_query(question_filtered))
        print()
        i += 1

def run_task(task_id):
    if task_id == 1:
        run_task_1()
    elif task_id == 2:
        run_inference_sample()


if __name__ == '__main__':
    fire.Fire(run_task)

    # print('Response: ', response, 'Ground Truth: ', sample_answer)
    # query = "What was the capital of the Safavid Dynasty ?"
    # key_word = filter_query_retrieval(query)
    # article_ids = search(key_word)
    # sample_data_dict = get_data_from_sample(SAMPLE_DATA_PATH)
    # get_accuracy(sample_data_dict)
