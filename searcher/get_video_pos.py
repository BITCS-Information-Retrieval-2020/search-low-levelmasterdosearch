from .Similarity.similarity_test import test_similarity
# from pprint import pprint

# def test_search(query):
#     s = Searcher_Tool(index_name='test', doc_type='papers')
#     search_info = {
#         'query_type': 'integrated_search',
#         'query': query,
#         'match': {
#             'title': True,
#             'abstract': True,
#             'paperContent': True,
#             'videoContent': False,
#         },
#         'filter': {
#             'yearfrom': 1000,
#             'yearbefore': 3000,
#         },
#         # 'sort': 'relevance',
#         'sort': 'year',
#     }
#     res, _, _ = s.search_paper_by_name(search_info)
#     videoContent = res[0]['videoContent']
#     return videoContent

def get_video_pos(query, videoContent, threshold=0.6):
    """Return a list of video captions related to user's query

    Args:
        query: english query text
        videoContent: a list of video caption information
        threshold: captions whose similarity score is > threshold is returned

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
    # print('query:' + query)
    # pprint(res_list)
    return res_list


if __name__ == '__main__':
    # from Searcher import Searcher
    query = 'integrated approach'
    videoContent = test_search(query)
    get_video_pos(query=query, videoContent=videoContent)
