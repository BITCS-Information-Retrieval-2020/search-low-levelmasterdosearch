from mdsearch import Searcher

S = Searcher(index_name='paperdb', doc_type='papers')

search_info = {
        'query_type': 'integrated_search',
        'query': 'pose',
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
        # 'sort': 'relevance',
        'sort': 'year', 
        'is_filter': False,
        'is_rescore': False,
        'is_cited': False
    }

paper, paper_id, paper_num = S.search_paper_by_name(search_info)

print(paper[0].keys())

video_pos = S.get_video_pos_by_paper_id(search_info, paper_id[0])

print(video_pos[0])

p_id = 'semisuperviseddialoguepolicylearningviastochasticrewardestimation'

video_pos = S.get_video_pos_by_paper_id(search_info, p_id)

print(video_pos)
