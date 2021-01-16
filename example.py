import pprint

from mdsearch import Searcher

S = Searcher()

# 综合检索
search_info_1 = {
    'query_type': 'integrated_search',
    'query': 'Attention Is All You Need',
    'match': {
        'title': True,
        'abstract': False,
        'paperContent': False,
        'videoContent': False,
        'authors': False
    },
    'filter': {
        'yearfrom': 1000,
        'yearbefore': 3000,
    },
    'sort': 'relevance',
    'is_filter': False,
    'is_rescore': False,
    'is_cited': False
}

paper, paper_id, paper_num = S.search_paper_by_name(search_info_1)

print('------Case 1:综合检索------')
for i in range(10):
    print(paper[i]['title'])

# 高级检索
search_info_2 = {
    'query_type': 'advanced_search',
    'match': {
        'title': 'attention',                            # 用户查询内容
        'abstract': None,
        'paperContent': None,
        'videoContent': None,
        'authors': "Ashish"
    },
    'filter': {
        'yearfrom': 1000,
        'yearbefore': 3000,
    },
    'sort': 'relevance',
    'is_filter': False,                             # 高级检索无论True还是False都不会进行过滤
    'is_rescore': False,
    'is_cited': False
}

paper, paper_id, paper_num = S.search_paper_by_name(search_info_2)

print('------Case 2:高级检索------')
for i in range(10):
    print(paper[i]['title'])

# 视频定位
search_info_3 = {
    'query_type': 'integrated_search',
    'query': 'dialog',
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
    'is_filter': False,
    'is_rescore': False,
    'is_cited': False
}

p_id = 'semisuperviseddialoguepolicylearningviastochasticrewardestimation'

video_pos = S.get_video_pos_by_paper_id(search_info_3, p_id)

print('------Case 3:高级检索------')
for p in video_pos:
    pprint(p)
