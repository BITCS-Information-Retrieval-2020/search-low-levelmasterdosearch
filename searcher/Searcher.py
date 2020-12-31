from elasticsearch5 import Elasticsearch
from datetime import datetime
import json


class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


class Searcher:
    """Searches papers from elasticsearch database

    Longer class information....
    Longer class information....

    """
    def __init__(self, index_name, doc_type, host='10.1.114.114', port=9200):
        """Initialize a search engine

        Args:
            host: A host name of elasticsearch
            port: A port number of elasticsearch
            index_name: name of the index you want to search for
            doc_type: name of the doc_type under certain index

        """
        self.es = Elasticsearch([{'host': host, 'port': port}])
        self.index = index_name
        self.doc_type = doc_type

    def generate_dsl(self, search_info):
        """Generate DSL given query and search settings
        Args:
            search_info: a dict including a query and other settings
        Example:
            {
                'query': 'hello world",
                'title': True,
                'abstract': True,
                'paper_content': False,
                'video_content': False,
                'yearfrom': 2019,
                'sort': 'relevance'
            }
        Return:
            dsl: a dsl translated from search info
        """
        dsl = Vividict()
        query = search_info['query']
        dsl['query']['bool']['must']['multi_match']['query'] = query
        fields = []
        if search_info['title']:
            fields.append('title^3')

        if search_info['abstract']:
            fields.append('abstract^2')

        if search_info['paper_content']:
            fields.append('paper_content')

        # elif search_info['video_content']:
        #     fields.append('video_content')

        dsl['query']['bool']['must']['multi_match']['fields'] = fields

        dsl['query']['bool']['should'] = []
        should = Vividict()
        should['range']['year']['gte'] = search_info['yearfrom']
        dsl['query']['bool']['should'].append(should)

        return dsl

    def search_paper_by_name(self, search_info):
        """Search paper by name

        Args:
            query: query string from user

        Retrun:
            res_list: A list of paper information
        """
        dsl = self.generate_dsl(search_info)
        res = self.es.search(index=self.index, doc_type=self.doc_type, body=dsl)
        res_list, num = get_paper_info(res)
        return res_list, num


def get_paper_info(res):
    """Return raw paper info given es search result

    Args:
        res: A dict of result from es.search

    Return:
        paper_list: A list of dicts, each dict stores information of a paper
        num: length of paper_list
    """
    paper_list = []
    hits = res['hits']['hits']
    num = res['hits']['total']
    for hit in hits:
        paper_list.append(hit['_source'])
    return paper_list, num


if __name__ == '__main__':
    s = Searcher(index_name='test', doc_type='papers')
    search_info = {
        'query': 'attention network',
        'title': True,
        'abstract': False,
        'paper_content': False,
        # 'video_content': False,
        'yearfrom': 2000,
        'sort': 'relevance'
    }
    res, num = s.search_paper_by_name(search_info)
    print(num)
    print(res)
