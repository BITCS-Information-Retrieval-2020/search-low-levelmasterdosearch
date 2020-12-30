import json
import requests
from tqdm import tqdm


class Embedding(object):
    def __init__(self):
        self.embedding_list = []
    
    def text_embedding(self, sentences):
        for sentence in tqdm(sentences):
            self.embedding_list.append(self.request_server(sentence))

        return self.embedding_list

    def request_server(self, sentence):
        resp = requests.post("localhost/textEmbedding",
                            data = {'sentence': sentence})
        text_embedding = resp.json()['text_embedding']     
        return text_embedding