import json
import requests


def test_embedding(sentence):
    '''
        sentence: English text input
        return: the embedding of sentence in json format
    '''
    try:
        resp = requests.post("localhost/textEmbedding", data={'sentence': sentence})
    except Exception:
        return "__ERROR__"
    else:
        text_embedding = resp.json()['text_embedding']

    return text_embedding


def test_similarity(que_sentence, que_list):
    '''
        que_sentence: query English text input
        que_list : text_embedding list
        return: similarity list
    '''
    try:
        que_list_js = json.dumps(que_list)
        resp = requests.post("http://101.124.42.4:1235/calSimilarity", data={'que_sentence': que_sentence, 'que_list': que_list_js})
    except Exception:
        return "__ERROR__"
    else:
        similarity_list = resp.json()['similarity_list']

    return similarity_list


if __name__ == '__main__':
    s_list = [
        "I am a little girl.",
        "Today is a nice day.",
        "Wow!",
        "I am fine Thank you.",
        "What a pity!",
        "I am not fine, not fine, not fine"
    ]
    e_list = []
    for s in s_list:
        e_list.append(test_embedding(s))
    que_sentence = "I am a little boy."

    similarity_list = test_similarity(que_sentence, e_list)
    print(similarity_list)
    que_sentence = "HAHA!"
    similarity_list = test_similarity(que_sentence, e_list)
    print(similarity_list)
