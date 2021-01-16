from elasticsearch5 import Elasticsearch
from pprint import pprint
from .Similarity.similarity_test import test_similarity
import json

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

class Searcher():
    """Searches papers from elasticsearch database

    Longer class information....
    Longer class information....

    """
    def __init__(self, index_name='paperdb', doc_type='papers', host='10.1.114.114', port=9200):
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
            Attention that 'query_type' must be consistent with 'match' !
        Example:
            {
                'query_type': 'integrated_search',
                'query': 'attention network',
                'match': {
                    'title': True,
                    'abstract': True,
                    'paperContent': True,
                    'videoContent': True,
                },
                'filter': {
                    'yearfrom': 1000,
                    'yearbefore': 3000,
                },
                'sort': 'year',
                'is_filter': True,
                'is_rescore': True,
                'is_cited': False
            }
            or
            {
                'query_type': 'advanced_search',
                'match': {
                    'title': 'attention',
                    'abstract': 'attention',
                    'paperContent': 'attention',
                    'videoContent': None,
                },
                'filter': {
                    'yearfrom': 1000,
                    'yearbefore': 3000,
                },
                'sort': 'relevance',
                'is_filter': False,
                'is_rescore': True,
                'is_cited': False
            }
        Return:
            dsl: a dsl translated from search info
        """

        # check search_info
        if 'integrated' in search_info['query_type']:
            assert 'query' in search_info, "Integrated search must have query !"
            assert isinstance(search_info['match']['title'], bool), "Here needs bool type !"
        else:
            assert isinstance(search_info['match']['title'], (str, None)), \
            "Here needs a string or None !"

        if search_info['is_cited'] is False:
            dsl = Vividict()
            dsl['query']['bool']['must'] = []
            dsl['query']['bool']['should'] = []
            dsl['rescore'] = []

            if 'integrated' in search_info['query_type']:
                match = self.get_integrated_match(search_info['query'], search_info['match'])
                dsl['query']['bool']['should'] = match
                if search_info['is_filter'] is True:
                    filter = self.get_filter_query(search_info['query'])
                    dsl['query']['bool']['must'].append(filter)
                if search_info['is_rescore'] is True:
                    rescore = self.get_rescore_query(match)
                    dsl['rescore'] = rescore

            else:  # 'advanced_search'
                match = self.get_advanced_match(search_info['match'])
                dsl['query']['bool']['must'] = match
                if search_info['is_rescore'] is True:
                    rescore = self.get_rescore_query(match)
                    dsl['rescore'] = rescore

            year_range = Vividict()
            year_range['range']['year']['gte'] = search_info['filter'].get('yearfrom', 1000)
            year_range['range']['year']['lte'] = search_info['filter'].get('yearbefore', 3000)
            dsl['query']['bool']['must'].append(year_range)

        else:  # cited-function_score
            dsl = Vividict()
            dsl['query']['function_score']['query']['bool']['must'] = []
            dsl['query']['function_score']['query']['bool']['should'] = []
            dsl['query']['function_score']['field_value_factor'] = []
            dsl['rescore'] = []

            if 'integrated' in search_info['query_type']:
                match = self.get_integrated_match(search_info['query'], search_info['match'])
                dsl['query']['function_score']['query']['bool']['should'] = match
                cited = self.get_function_factor()
                dsl['query']['function_score']['field_value_factor'] = cited
                if search_info['is_filter'] is True:
                    filter = self.get_filter_query(search_info['query'])
                    dsl['query']['function_score']['query']['bool']['must'].append(filter)
                if search_info['is_rescore'] is True:
                    rescore = self.get_rescore_query(match)
                    dsl['rescore'] = rescore

            else:  # 'advanced_search'
                match = self.get_advanced_match(search_info['match'])
                dsl['query']['bool']['must'] = match
                if search_info['is_rescore'] is True:
                    rescore = self.get_rescore_query(match)
                    dsl['rescore'] = rescore

            year_range = Vividict()
            year_range['range']['year']['gte'] = search_info['filter'].get('yearfrom', 1000)
            year_range['range']['year']['lte'] = search_info['filter'].get('yearbefore', 3000)
            dsl['query']['function_score']['query']['bool']['must'].append(year_range)

        if search_info['sort'] == 'year':
            dsl['sort']['year'] = 'desc'
        elif search_info['sort'] == 'cited':
            dsl['sort']['cited'] = 'asc'

        return dsl

    def get_integrated_match(self, query, match):
        """get match of intergrated search

        Args:
            query: query string from user
            match: A dict contained title, abstract...

        Return:
            res: A list of match
        """
        res = []

        if match['title'] or match['abstract']:
            tmp = Vividict()
            tmp['multi_match']['query'] = query

            fields = []
            if match['title']:
                fields.append('title^3')

            if match['abstract']:
                fields.append('abstract^2')

            tmp['multi_match']['fields'] = fields
            res.append(tmp)

        if match['paperContent']:
            nest = self.get_nested_query_paperContent(query)
            res.append(nest)

        if match['videoContent']:
            nest = self.get_nested_query_videoContent(query)
            res.append(nest)

        if match['authors']:
            nest = self.get_nested_query_authors(query)
            res.append(nest)

        return res

    def get_advanced_match(self, match):
        """get match of advanced search

        Args:
            match: A dict contained title, abstract, paper_content...

        Return:
            res: A list of match
        """
        res = []
        if match['title']:
            _match = {'match': {'title': match['title']}}
            res.append(_match)

        if match['abstract']:
            _match = {'match': {'abstract': match['abstract']}}
            res.append(_match)

        if match['paperContent']:
            nest = self.get_nested_query_paperContent(match['paperContent'])
            res.append(nest)

        if match['videoContent']:
            nest = self.get_nested_query_videoContent(match['videoContent'])
            res.append(nest)

        if match['authors']:
            nest = self.get_nested_query_authors(match['authors'])
            res.append(nest)

        return res

    def get_nested_query_authors(self, query):

        nest = Vividict()
        nest['nested']['path'] = 'authors'
        nest['nested']['score_mode'] = 'max'

        tmp = Vividict()
        fields = ['authors.firstName', 'authors.lastName']
        tmp['multi_match']['fields'] = fields
        tmp['multi_match']['query'] = query
        nest['nested']['query']['bool']['must'] = tmp

        return nest

    def get_nested_query_paperContent(self, query):

        nest = Vividict()
        nest['nested']['path'] = 'paperContent'
        nest['nested']['score_mode'] = 'max'

        tmp = Vividict()
        fields = ['paperContent.text', 'paperContent.subtitles^2', 'paperContent.subtexts']
        tmp['multi_match']['fields'] = fields
        tmp['multi_match']['query'] = query
        nest['nested']['query']['bool']['must'] = tmp

        return nest

    def get_nested_query_videoContent(self, query):

        nest = Vividict()
        nest['nested']['path'] = 'videoContent'
        nest['nested']['score_mode'] = 'max'

        tmp = Vividict()
        tmp['match']['videoContent.textEnglish'] = query
        nest['nested']['query']['bool']['must'] = tmp

        return nest

    def get_function_factor(self):
        cited = Vividict()
        cited['field'] = 'cited'
        cited['modifier'] = 'log1p'
        cited['factor'] = 0.5
        cited['missing'] = 0

        return cited

    def get_filter_query(self, query):
        filter = Vividict()
        tag_list = []
        word_list = query.split()
        for word in word_list:
            tag_list.append(word.capitalize())
            tag_list.append(word.lower())
        filter['terms']['abstract'] = tag_list

        return filter

    def get_rescore_query(self, match):
        rescore = Vividict()
        rescore['window_size'] = 100
        rescore['query']['rescore_query'] = match[0]
        rescore['query']['query_weight'] = 1.5
        rescore['query']['rescore_query_weight'] = 0.5

        return rescore

    def search_paper_by_name(self, search_info, only_top_k=True, size=100):
        """Search paper by name
        Args:
            query: query string from user

        Return:
            paper_list: A list of paper information
            paper_id  : A list of paper id
            paper_num : The number of returned paper
        """
        dsl = self.generate_dsl(search_info)
        result = self.es.search(index=self.index, doc_type=self.doc_type, body=dsl, size=size)
        return self.get_paper_info(result)

    def get_video_pos_by_paper_id(self, search_info, paper_id, threshold=0.6):
        """
        Args:
            search_info: the same as that in self.generate_dsl()
            paper_id: A string, given by es

        Return:
            a sorted video captions' list according to similarity between
            captions and query
        """
        
        assert isinstance(paper_id, str), "paper_id must be a string, here need only one id !"

        paper = self.es.get_source(index=self.index, doc_type=self.doc_type, id=paper_id)

        return self.get_video_pos_by_paper(search_info=search_info,
                                           paper=paper,
                                           threshold=threshold)

    def get_video_pos_by_paper(self, search_info, paper, threshold=0.6):
        """
        Args:
            paper: A dict contained title, abstract ...

        Return:
            a sorted video captions' list according to similarity between
            captions and query
        """

        assert isinstance(paper, dict), "paper must be a dict, here need only one paper !"

        if 'integrated' in search_info['query_type']:
            query = search_info['query']
        else:
            query = search_info['match']['videoContent']

        assert (query is not None)

        if 'videoContent' not in paper:
            return [None]

        pos = self.get_video_pos(query=query,
                            videoContent=paper['videoContent'],
                            threshold=threshold)
        return pos

    @staticmethod
    def get_paper_info(res):
        """Return raw paper info given es search result
        Args:
            res: A dict of result from es.search

        Return:
            paper_list: A list of dicts, each dict stores information of a paper
            num: length of paper_list
        """
        paper_list = []
        paper_id = []
        hits = res['hits']['hits']
        num = res['hits']['total']
        # import pdb; pdb.set_trace();
        for hit in hits:
            paper_list.append(hit['_source'])
            paper_id.append(hit['_id'])
        return paper_list, paper_id, num

    @staticmethod
    def remove_text_embedding(papers):
        """Remove textEmbedding in videoContent
        Args:
            papers: A list of paper
        """
        for paper in papers:
            if 'videoContent' in paper:
                for v in paper['videoContent']:
                    if 'textEmbedding' in v:
                        v.pop('textEmbedding')
    @staticmethod
    def get_video_pos(query, videoContent, threshold=0.6):
        """Return a list of video captions related to user's query

        Args:
            query: english query text
            videoContent: a list of video caption information
            threshold: captions whose similarity score is > threshold are returned

        Return:
            res_list: a sorted video captions' list according to similarity between
                    captions and query
        """
        emd_list = [v.pop('textEmbedding') for v in videoContent]
        sim_list = test_similarity(query, emd_list)
        if sim_list == '__ERROR__':
            return sim_list

        res_list = []
        for s, v in zip(sim_list, videoContent):
            v['score'] = s
            if v['score'] > threshold:
                res_list.append(v)
            elif query in v['textEnglish']:
                res_list.append(v)
        # print('query:' + query)
        # pprint(res_list)
        return res_list


if __name__ == '__main__':

   print('wo ta ya ya de fo le')
