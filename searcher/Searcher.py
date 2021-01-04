from elasticsearch5 import Elasticsearch
from pprint import pprint

# from get_video_pos import get_video_pos
from get_video_pos import *


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
            }
        Return:
            dsl: a dsl translated from search info
        """
        dsl = Vividict()
        dsl['query']['bool']['must'] = []
        dsl['query']['bool']['should'] = []

        if 'integrated' in search_info['query_type']:
            match = self.get_integrated_match(search_info['query'], search_info['match']) 
            dsl['query']['bool']['should'] = match
        else: # 'advanced_search'
            match = self.get_advanced_match(search_info['match'])
            dsl['query']['bool']['must'] = match
            
        year_range = Vividict()
        year_range['range']['year']['gte'] = search_info['filter'].get('yearfrom', 1000)
        year_range['range']['year']['lte'] = search_info['filter'].get('yearbefore', 3000)
        dsl['query']['bool']['must'].append(year_range)

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

        return res

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


    def search_paper_by_name(self, search_info):
        """Search paper by name
        Args:
            query: query string from user

        Return:
            res_list: A list of paper information
            num: The number of returned paper
            video_pos(optional): A list of video pos of all papers
        """
        dsl = self.generate_dsl(search_info)
        res = self.es.search(index=self.index, doc_type=self.doc_type, body=dsl)
        res_list, paper_id, num = self.get_paper_info(res)

        return res_list, paper_id, num

    def get_video_pos_by_paper_id(self, search_info, paper_id, threshold=0.6):
        """
        Args:
            search_info: the same as that in self.generate_dsl()
            paper_id: A string, given by es

        Return:
            a sorted video captions' list according to similarity between
            captions and query
        """

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

        if 'integrated' in search_info['query_type']:
            query = search_info['query']
        else:
            query = search_info['match']['videoContent']

        if 'videoContent' not in paper:
            return [None]

        pos = get_video_pos(query=query,
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


if __name__ == '__main__':

    s = Searcher(index_name='test', doc_type='papers')

    # 综合检索
    search_info = {
        'query_type': 'integrated_search',
        'query': 'pose',
        'match': {
            'title': True,
            'abstract': False,
            'paperContent': True,
            'videoContent': False,
        },
        'filter': {
            'yearfrom': 1000,
            'yearbefore': 3000,
        },
        # 'sort': 'relevance',
        'sort': 'year',
    }
    # 高级检索
    search_info_2 = {
        'query_type': 'advanced_search',
        'match': {
            'title': 'estimating',
            'abstract': 'RGB',
            'paperContent': 'pose',
            'videoContent': 'pixel',
        },
        'filter': {
            'yearfrom': 1000,
            'yearbefore': 3000,
        },
        # 'sort': 'relevance',
        'sort': 'year',
    }

    res, paper_id, num = s.search_paper_by_name(search_info_2)
    print(num)
    pprint(paper_id)

    video_pos = s.get_video_pos_by_paper_id(search_info_2, paper_id[0])
    pprint(video_pos)

    s.remove_text_embedding(res)
    res[0].pop('paperContent')
    res[0].pop('references')
    res[0].pop('videoContent')
    pprint(res[0])

    for e in res:
        print(e['year'])
