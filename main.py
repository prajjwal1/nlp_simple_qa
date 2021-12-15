import fire
from tqdm import tqdm

from _filter import filter_query, filter_query_retrieval
from dataset_utils import (
    expand_query,
    get_accuracy,
    get_data_from_sample,
    get_dependencies,
    get_lemmas,
    get_pos_tags,
    get_wordnet_features,
    remove_stopwords,
    sample_check,
)
from embeddings import get_best_sentence
from indexer import search

SAMPLE_DATA_PATH = "data/qa_data.txt"
SAMPLE_DATA_VALIDATION = "data/sample_check/sample.xlsx"


def run_inference_sample():
    questions, answers, complexity_levels = sample_check(SAMPLE_DATA_VALIDATION)
    correct = 0
    easy, medium, hard = 0, 0, 0
    easy_total, medium_total, hard_total = 0, 0, 0
    for sample_question, sample_answer, sample_comp_level in tqdm(
        zip(questions, answers, complexity_levels)
    ):
        filtered_query = filter_query_retrieval(sample_question)
        # retrieved_article_text = search(filtered_query, highlight=True)
        # response = filter_query(get_best_sentence(sample_question, retrieved_article_text))
        retrieved_article_id = search(filtered_query)
        best_sentence, _ = get_best_sentence(sample_question, retrieved_article_id)
        response = filter_query(best_sentence)
        sample_answer = filter_query(sample_answer)

        print(
            "\nQuestion: ",
            sample_question,
            "\nResponse: ",
            response,
            "\nGround Truth: ",
            sample_answer,
            "\nComplexity: ",
            sample_comp_level,
        )
        print("==================================================================================")

        if str(sample_answer) in response:
            correct += 1
            if sample_comp_level == 1:
                easy += 1
            elif sample_comp_level == 2:
                medium += 1
            else:
                hard += 1
        if sample_comp_level == 1:
            easy_total += 1
        elif sample_comp_level == 2:
            medium_total += 1
        else:
            hard_total += 1

    print("\nAccuracy: ", correct / len(questions))
    print(
        "\nAccuracy on Easy: ",
        easy / easy_total,
        "Easy correctly classified: ",
        easy,
        "Total correct: ",
        easy_total,
    )
    print(
        "\nAccuracy on Medium: ",
        medium / medium_total,
        "Medium correctly classified: ",
        medium,
        "Total medium: ",
        medium_total,
    )
    print(
        "\nAccuracy on Hard: ",
        hard / hard_total,
        "Hard correctly classified: ",
        hard,
        "Total hard: ",
        hard_total,
    )


def inference_test(FILE_PATH):
    file1 = open(FILE_PATH, "r")
    file2 = open("output.csv", "w")
    questions = file1.readlines()
    for question in tqdm(questions):
        filtered_query = filter_query_retrieval(str(question))
        retrieved_article_id = search(filtered_query)
        best_sentence, best_article_id = get_best_sentence(question, retrieved_article_id)
        question = question.replace("\n", "")
        val_str = f"{question}, '{best_article_id}', '{best_sentence}'"
        file2.write(val_str + "\n")
    file2.close()
    print("output.csv file created successfully")


def run_task_1():
    questions, _, _ = sample_check(SAMPLE_DATA_VALIDATION)
    questions = [
        q.lower()
        .replace('"', "")
        .replace("?", "")
        .replace(".", "")
        .replace("“", "")
        .replace("”", "")
        .replace("!", "")
        .replace("-", "")
        .replace("—", "")
        .replace(";", "")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "")
        .replace("\\", "")
        .replace("\n", "")
        .replace("\t", "")
        .replace("\r", "")
        for q in questions
    ]
    i = 1
    for question in questions:
        print(f"Question #{i}:", question)
        question_filtered = remove_stopwords(question)
        print("POS Tagged:", get_pos_tags(question))
        print("Dependency Parsed:", get_dependencies(question))
        print("Word Filter:", question_filtered)
        print("Lemmatized:", get_lemmas(question_filtered))
        print("Hypernyms:", get_wordnet_features(question_filtered, "hypernyms"))
        print("Hyponyms:", get_wordnet_features(question_filtered, "hyponyms"))
        print("Meronyms", get_wordnet_features(question_filtered, "meronyms"))
        print("Holonyms", get_wordnet_features(question_filtered, "holonyms"))
        print("Synonyms:", expand_query(question_filtered))
        print()
        print("======================================")
        i += 1


def run_task(task_id, file_path=None):
    if task_id == 1:
        run_task_1()
    elif task_id == 2:
        run_inference_sample()
    elif task_id == 3:
        inference_test(file_path)


if __name__ == "__main__":
    fire.Fire(run_task)

    # print('Response: ', response, 'Ground Truth: ', sample_answer)
    # query = "What was the capital of the Safavid Dynasty ?"
    # key_word = filter_query_retrieval(query)
    # article_ids = search(key_word)
    #  sample_data_dict = get_data_from_sample(SAMPLE_DATA_PATH)
    #  get_accuracy(sample_data_dict)
