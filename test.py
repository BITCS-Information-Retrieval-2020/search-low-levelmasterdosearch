from searcher import *
from pprint import pprint
import time


S = Searcher(index_name='paperdb', doc_type='papers')

search_info = {
        'query_type': 'integrated_search',
        'query': 'Ashish',
        'match': {
            'title': False, 
            'abstract': False,
            'paperContent': False,
            'videoContent': False,
            'authors': True,
        },
        'filter': {
            'yearfrom': 1000,
            'yearbefore': 3000,
        },
        'sort': 'relevance',
        # 'sort': 'year', 
        'is_filter': False,
        'is_rescore': False,
        'is_cited': False
    }

# 高级检索
search_info_2 = {
        'query_type': 'advanced_search',
        'match': {
            'title': 'attention is all you need',
            'abstract': None,
            'paperContent': None, #'pose',
            'videoContent': None, #'pose',
            'authors': None, #'Ashish',
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

# test time

# hhh = 'Learning to follow instructions is of fundamental importance to autonomous agents for vision-and-language navigation. In this paper, we study how an agent can navigate long paths when learning from a corpus that consists of shorter ones. We show that existing'
# hhh = hhh.split()
# # print(len(hhh))

# begin = time.time()

# k = 100
# for i in range(k):
# 	i = i % 20
# 	query = hhh[i*2] + ' ' + hhh[i*2+1]
# 	# print(query)
# 	search_info['match']['query'] = query
# 	_ = S.search_paper_by_name(search_info, k=100)

# end = time.time()

# print()
# print('Total number of random query:', k)
# print('Time of per query:',(end-begin)/k)
# print()

paper, paper_id, paper_num = S.search_paper_by_name(search_info, size=100)
print(len(paper), paper_num)
# print(paper[0].keys())
# print('\nResult of query string:', search_info['query'])
for i in range(30):
	print('\nTitle:', i, paper[i]['title'])
# print(paper[0]['authors'])

# print('\nAbstract:', paper[0]['abstract'])
# print()
# p_id = 'semisuperviseddialoguepolicylearningviastochasticrewardestimation'
# video_pos = S.get_video_pos_by_paper_id(search_info_2, p_id)
# pprint(video_pos[0])
