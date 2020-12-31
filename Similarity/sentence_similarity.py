import torch
from scipy.spatial.distance import cosine
from transformers import BertModel, BertTokenizer
import os


class SentenceSimilarity:

    def __init__(self, model_path='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertModel.from_pretrained(model_path)
        self.model.eval()
        self.device = torch.device('cuda:0')
        self.model = self.model.to(self.device)

    def text_to_tensor(self, text):
        text = text.strip().lower()
        tokens = self.tokenizer.tokenize(text)
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        tokens_ids = self.tokenizer.build_inputs_with_special_tokens(tokens_ids)
        tokens_tensor = torch.tensor([tokens_ids])
        return tokens_tensor

    def get_embedding(self, sent):
        tokens_tensor = self.text_to_tensor(sent)
        tokens_tensor = tokens_tensor.to(self.device)
        with torch.no_grad():
            output = self.model(tokens_tensor)[0]
        embedding = output[0].mean(dim=0).cpu().numpy()
        return embedding

    def similarity(self, emb1, emb2):
        return cosine(emb1, emb2)


if __name__ == '__main__':

    ss = SentenceSimilarity()
    s1 = 'I am a girl'
    s2 = 'I am a boy'
    s3 = 'Thank you'
    print("1")
    e1 = ss.get_embedding(s1)
    print(type(e1))
    e2 = ss.get_embedding(s2)
    e3 = ss.get_embedding(s3)
    print("2")
    print(1 - ss.similarity(e1, e2))
    print(1 - ss.similarity(e1, e3))
    print("3")
