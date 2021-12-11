import pickle

def filter_query(query):
    words_to_remove = ["how", "when", "what", "was", "the", "of", "the", "\""]
    chars_to_remove = ['"', '?', '.']
    query = ' '.join([x for x in query.split() if x not in words_to_remove])
    for char in chars_to_remove:
        query = query.replace(char, "")
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
    first_max = freqs_each_token.index(min(freqs_each_token))
    #  second_max = freqs_each_token.index(sorted(freqs_each_token)[1])

    return query_list[first_max] #, query_list[second_max]

