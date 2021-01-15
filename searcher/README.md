#### 接口文档

##### 0   整体流程为通过search_info封装用户的查询内容，然后调用相关API返回检索结果。

##### 1   初始化

```python
import Searcher
S = Searcher(index_name='paperdb', doc_type='papers')
```

##### 2   检索论文

```python
paper, paper_id, paper_num = S.search_paper_by_name(search_info)
```

```python 
返回结果说明：
paper_num   : A int number of paper.
paper_id    : A list of string, each string means paper id.
paper       : A list of dicts, each dict stores information of a paper.
```



##### 3   检索单个论文视频中的相关内容(可通过前一步检索论文返回的paper_id或者paper，注意是单个)

```python
video_pos = S.get_video_pos_by_paper_id(search_info, paper_id)
video_pos = S.get_video_pos_by_paper(search_info, paper)
```

##### 4   search_info 格式

```python
# 综合检索
    search_info = {
        'query_type': 'integrated_search',
        'query': string,                                # 用户查询的内容
        'match': {
            'title': bool,                              # True/False表示是否检索这个字段的内容
            'abstract': bool,
            'paperContent': bool,
            'videoContent': bool,
        },
        'filter': {
            'yearfrom': 1000,                           # paper的年份限制
            'yearbefore': 3000,
        },
        # 'sort': 'relevance',
        'sort': 'year',                                 # 排序方式：year/cited/relevance
        'is_filter': False,                             # 是否先过滤后排序，建议True，提升检索效率
        'is_rescore': False,                            # 是否采用重排序，依据relevance排序时建议True，增强排序效果
        'is_cited': False                               # 是否使用引用量参与排序，由于未爬取引用量字段，只能为False
    }
# 高级检索
    search_info_2 = {
        'query_type': 'advanced_search',
        'match': {
            'title': string,                            # 用户查询内容
            'abstract': string,                         # 若不含有某项，设置成 None/False
            'paperContent': string,
            'videoContent': string,
        },
        'filter': {
            'yearfrom': 1000,
            'yearbefore': 3000,
        },
        'sort': 'year',
        'is_filter': False,                             # 高级检索无论True还是False都不会进行过滤
        'is_rescore': False,
        'is_cited': False
    }
```

