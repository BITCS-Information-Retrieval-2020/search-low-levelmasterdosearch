from flask import Flask, jsonify, request
from sentence_similarity import SentenceSimilarity
import json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

SS = SentenceSimilarity()


def get_embedding(sentence):
    tmp_embedding = SS.get_embedding(sentence).tolist()
    json_embedding = json.dumps(tmp_embedding)
    return json_embedding


@app.route('/textEmbedding', methods=['POST'])
def textEmbedding():
    if request.method == 'POST':
        sentence = request.form['sentence']
        text_embedding = get_embedding(sentence)
        return jsonify({'text_embedding': text_embedding})


def get_similarity(que_sentence, que_list):
    '''
        que_sentence: 查询句子文本
        que_list: embedding列表
        result_similarity: 查询句子与que_list以此比较得到的相似度
    '''
    result_similarity = []
    que_embedding = SS.get_embedding(que_sentence).tolist()
    for item in que_list:
        item_embedding = json.loads(item)
        item_similarity = 1 - SS.similarity(que_embedding, item_embedding)
        result_similarity.append(item_similarity)

    return result_similarity


@app.route('/calSimilarity', methods=['POST'])
def calSimilarity():
    if request.method == 'POST':
        que_sentence = request.form['que_sentence']
        que_list_js = request.form['que_list']
        que_list = json.loads(que_list_js)
        similarity_list = get_similarity(que_sentence, que_list)
        return jsonify({'similarity_list': similarity_list})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=0000, debug=False)
