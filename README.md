# Search-low-levelmasterdosearch

[TOC]

## 项目介绍

暂时不写



## 小组分工

|    姓名     | 学号 | 分工 |
| :---------: | :--: | :--: |
| [@朱婧婧]() |      |      |
| [@熊婧雯]() |      |      |
| [@赫宇欣]() |      |      |
| [@姚潇翛]() |      |      |
| [@程文浩]() |      |      |
| [@李易为]() |   3120205496   |   检索优化   |
|  [@孙昊]()  |   3120205524   |   字幕翻译   |

//自己填



## 版本说明

ElasticSearch 5.0.0

//依赖的第三方库和包版本

//汇总后再写



## 仓库结构

- Data：
- pdfToJson：

//暂时不写



## 代码调用

//部署过程，启动运行流程

//汇总后再写



## 数据格式

### 存储字段

文献数据保存在`paperdb.papers`中，一篇文献的存储字段如下：

```json
{
	"_id": "deeprewiringtrainingverysparsedeepnetworks",
	"arxiv_id": "arXiv:1711.05136",
	"title": "Deep Rewiring: Training very sparse deep networks",
	"authors": [{
			"firstName": "Guillaume",
			"lastName": "Bellec"
		},
		{
			"firstName": "David",
			"lastName": "Kappel"
		},
		{
			"firstName": "Wolfgang",
			"lastName": "Maass"
		},
		{
			"firstName": "Robert",
			"lastName": "Legenstein"
		}
	],
	"year": "2017",
	"publisher": "arXiv",
	"cited": "11",
	"keywords": ["keyword1", "keyword2"],
	"abstract": "Neuromorphic hardware tends to pose limits on the connectivity of deepnetworks that one can run on them. But also generic hardware and ...",
	"subjects": "Neural and Evolutionary Computing (cs.NE)",
	"paperUrl": "https://arxiv.org/pdf/1711.05136",
	"paperPdfUrl": "https://arxiv.org/pdf/1711.05136.pdf#pdfjs.action=download",
	"paperPath": "/home/work/crawler/paper/deeprewiringtrainingverysparsedeepnetworks.pdf",
	"paperContent": {
		"text": "Network connectivity is one of the main determinants for whether a neural network can be efficiently implemented in hardware or ...",
		"subtitles": [
			"1 INTRODUCTION",
			"2 REWIRING IN DEEP NEURAL NETWORKS",
			"3 EXPERIMENTS",
			"4 CONVERGENCE PROPERTIES OF DEEP R AND SOFT-DEEP R",
			"5 DISCUSSION"
		],
		"subtexts": [
			["paragraph 1.1", "paragraph 1.2"],
			["paragraph 2.1", "paragraph 2.2", "paragraph 2.3"],
			["paragraph 3.1", "paragraph 3.2"],
			["paragraph 4.1", "paragraph 4.2", "paragraph 4.3"],
			["paragraph 5.1", "paragraph 5.2"]
		]
	},
	"references": [{
		"refTitle": "Fine-grained analysis of sentence embeddings using auxiliary prediction tasks",
		"refAuthors": [{
				"firstName": "Yossi",
				"lastName": "Adi"
			},
			{
				"firstName": "Einat",
				"lastName": "Kermany"
			},
			{
				"firstName": "Yonatan",
				"lastName": "Belinkov"
			},
			{
				"firstName": "Ofer",
				"lastName": "Lavi"
			},
			{
				"firstName": "Yoav",
				"lastName": "Goldberg"
			}
		],
		"refYear": "2017",
		"refPublisher": ""
	}],
	"videoUrl": "https://...",
	"videoContent": {
		"startTime": ["time1", "time3", "time5"],
		"endTime": ["time2", "time4", "time6"],
		"textEmbedding": ["vector1", "vector2", "vector3"],
		"textEnglish": ["haha", "hehe", "heihei"],
		"textChinese": ["哈哈", "呵呵", "嘿嘿"]
	},
	"codeUrl": "https://...",
	"datasetUrl": "https://..."
}
```

### 字段含义

|     字段      |  类型   |           说明           | 是否为集合 | 是否索引 |
| :-----------: | :-----: | :----------------------: | :--------: | :------: |
|     title     |  text   |         文献标题         |     ×      |    √     |
|    authors    | nested  |         文献作者         |     √      |    √     |
|   firstName   | keyword |          作者名          |     ×      |    √     |
|   lastName    | keyword |          作者姓          |     ×      |    √     |
|     year      | keyword | 文献发表年份（YYYY格式） |     ×      |    √     |
|   publisher   | keyword |       文献发表期刊       |     ×      |    √     |
|     cited     | integer |      文献被引用次数      |     ×      |    ×     |
|   keywords    | keyword |          关键词          |     √      |    √     |
|   abstract    |  text   |         文献摘要         |     ×      |    √     |
|   subjects    | keyword |       文献所属类别       |     √      |    √     |
|   paperUrl    | keyword |         文献链接         |     ×      |    ×     |
|  paperPdfUrl  | keyword |       文献下载链接       |     ×      |    ×     |
|   paperPath   | keyword |     文献在本地的位置     |     ×      |    ×     |
| paperContent  | nested  |       文献正文内容       |     ×      |    √     |
|     text      |  text   |         文献正文         |     ×      |    √     |
|   subtitles   |  text   |         段落标题         |     √      |    √     |
|   subtexts    |  text   |         段落内容         |     √      |    √     |
|  references   | nested  |           引用           |     ×      |    √     |
|   refTitle    |  text   |     被引用文献的标题     |     ×      |    √     |
|  refAuthors   | nested  |     被引用文献的作者     |     √      |    √     |
|    refYear    | keyword |   被引用文献的发表年份   |     ×      |    √     |
| refPublisher  | keyword |   被引用文献的发表期刊   |     ×      |    √     |
|   videoUrl    | keyword |         视频链接         |     ×      |    ×     |
|   videoPath   | keyword |     视频在本地的位置     |     ×      |    ×     |
| videoContent  | nested  |         视频内容         |     ×      |    √     |
|   startTime   | keyword |     每句字幕起始时间     |     √      |    ×     |
|    endTime    | keyword |     每句字幕结束时间     |     √      |    ×     |
| textEmbedding | keyword |       单句字幕向量       |     √      |    ×     |
|  textEnglish  |  text   |     单句字幕（英文）     |     √      |    √     |
|  textChinese  |  text   |     单句字幕（中文）     |     √      |    ×     |
|    codeUrl    | keyword |         代码链接         |     ×      |    ×     |
|  datasetUrl   | keyword |        数据集链接        |     ×      |    ×     |

### 附加说明

1. ElasticSearch中每条数据以JSON格式存储。这意味着除了_id，其他用户自定义的字段都可以“不存在”，上述例子中的存储字段是最完整的版本。

2. 当字段类型为`text`时，它会被分词以支持全文检索。而当字段类型为`keyword`时，它会按照精确值进行过滤、排序、聚合等操作。

3. 当字段的`index`设为`false`时，表示不支持检索，通常用于网页链接。

4. `title`字段支持“部分匹配”的检索。这意味着即使不输入完整的单词，也能匹配到相关数据。例如可以用前缀"integra"检索到文献"**Integration** of Leaky-Integrate-and-Fire-Neurons in Deep Learning Architectures"。

5. `nested`类型的字段支持嵌套检索，例如可以用`"match": { "authors.last":  "Ji" }`检索所有姓`Ji`的作者。

   

## 功能概要

### 检索

|    功能    | 函数名 | 输入 | 输出 |
| :--------: | :----: | :--: | :--: |
| 按标题检索 |        |      |      |
|            |        |      |      |

// hyx cwh lyw



### pdf抽取

PDF抽取模块的作用是从下载到本地的PDF文件中抽取结构化数据，以JSON格式保存，供检索使用。该模块主要分为以下两部分：

1. PDF转XML：[GROBID](https://github.com/kermitt2/grobid)是一个机器学习库，用于将原始文档（如PDF）提取、解析和重新构造为结构化XML/TEI编码的文档。在服务器安装并运行GROBID Server后，向指定`ip:port`提交PDF文档后，可以返回XML文档。
2. XML转JSON：`xmlToJson.py`文件封装了从XML文档中抽取信息，重新构造为JSON格式数据的功能。

#### 数据格式

从一篇文献的PDF中抽取得到的JSON数据如下：

```json
{
    "title": "title of a paper",
 	"authors": [
        {
            "firstName": "firstName of an author",
            "lastName": "lastName of an author "
        }
    ],
    "keywords":["keyword1","keyword2"],
    "abstract": "abstract of a paper",
    "paperContent":{
        "text": "all content of a paper (This is also a concatenation of subtexts)",
        "subtitles": [
            "1 INTRODUCTION",
            "2 REWIRING IN DEEP NEURAL NETWORKS",
            "3 EXPERIMENTS",
            "4 CONVERGENCE PROPERTIES OF DEEP R AND SOFT-DEEP R",
            "5 DISCUSSION"
        ],
        "subtexts":[
            ["paragraph 1.1", "paragraph 1.2"],
            ["paragraph 2.1", "paragraph 2.2", "paragraph 2.3"],
            ["paragraph 3.1", "paragraph 3.2"],
            ["paragraph 4.1", "paragraph 4.2", "paragraph 4.3"],
            ["paragraph 5.1", "paragraph 5.2"],
        ]
    },
    "references":[
        {
            "refTitle": "title of a reference paper",
            "refAuthors": [
                {
                    "firstName": "firstName of an author",
                    "lastName": "lastName of an author "
                }
            ],
            "refYear": "publised year of a reference paper",
        }
    ]
}
```

#### 使用方法	

1. 安装依赖包

   ```shell
   pip install -r requirements.txt
   ```

2. 从`pdfClient.py`文件中引用`grobid_client`

   ```python
   from pdfClient import grobid_client
   ```

3. 初始化一个PDF处理客户端实例，可以通过config文件修改GROBID Server处理PDF的参数

   ```python
   pdfClient = grobid_client(config_path = config_path)
   ```

4. 向`process_pdf`函数传入待处理的PDF文件路径，输出JSON格式的结构化数据

   ```python
   jsonData = pdfClient.process_pdf(pdf_path)
   ```



### 视频解析

//yxx sh
//转中文字幕部分

|    功能    | 函数名 | 输入 | 输出 |
| :--------: | :----: | :--: | :--: |
| 转中文字幕（Baidu） |  __parse_chinese_baidu  |   英文字母subtitle：list   |   中文字幕chineselist：list   |
| 转中文字幕（Google）| __parse_chinese_google |   英文字母subtitle：list   |   中文字幕chineselist：list   |

通过两种 API的调用，实现了英文字母转中文字幕的需求



## 统计信息

//cwh lyw

//数据统计、性能统计



## 与爬虫模块的连接

//xjw zjj

### 同步命令

#### 爬虫端

为MongoDB中数据库创建replica set

1. 启动服务

   ```shell
   mongod --dbpath /data/mongodb/db/ --replSet rs0
   ```

2. 进入对应数据库

   ```
   ./mongo
   use <DBName>
   rs.initiate()
   ```

#### 检索端

1. 安装相关包

   ```shell
   pip install mongo-connector[elastic5]
   pip install elastic2-doc-manager[elastic5]
   ```

2. 使用同步命令

   ```shell
   mongo-connector -m <ip1>:<port1> -t <ip2>:<port2> -d elastic2_doc_manager -n lowermaster.crawler -g paperdb.papers
   ```

   - -m：MongoDB的IP地址和端口
   - -t：ElasticSearch的IP地址和端口
   - -n：MongoDB中数据库名称
   - -g：ElasticSearch中数据库名称



## 与展示模块的连接

//hyx cwh lyw

//怎么打包的包，前端怎么调用



## 待完成的功能

//都可以写



## 特别说明
# 只有聪明的人才能看到代码
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>


# 检索模块
## 项目简介
搭建一个学术论文的综合搜索引擎，用户可以检索到一篇论文的综合信息，不仅有pdf文件，还有oral视频，数据集，源代码等多模态信息。  
从MongoDB中读取爬虫爬到的数据，建立索引，实现综合检索。
## 队伍名称
search-low-levelmasterdosearch
## 项目成员
朱婧婧 熊婧雯 赫宇欣 姚翛潇 程文浩 李易为 孙昊
## 注意事项
1. 项目成员编写代码时，建立以自己名字命名的分支，代码编写后需pull request, 不可直接提交到master分支上
2. 项目成员更新代码后，在readme中加入必要的说明
3. 测试文件、大文件请勿上传（写入.gitignore）
4. 所有提交的代码，必须经过flake8的检验
## 数据库版本
1. elasticsearch 5.5.3
2. mongodb 3.6.21
## 数据字段
./others/mongoDB.json
1. _id DOI或者arxiv编号
2. title 文章标题
3. authors 列表类型，每个作者包括firstName字段和lastName字段（复杂名字统一归到firstName里）
4. year YYYY格式
5. publisher 发表期刊（对期刊进行实体对齐，给检索模块返回一个期刊列表集合）
6. keywords 可能为空（检索模块提供）
7. abstract 优先使用网站上的爬取结果（爬虫提供）；否则写入pdf解析结果（检索提供）
8. subjects 论文分类（arxiv）
9. paperUrl 论文在网上的url
10. paperPath 论文的相对路径
11. paperContent 论文pdf解析后的内容，text 全文内容，subtitiles 章节标题，subtexts 章节内容（检索模块提供）
12. references 参考文献，列表格式，包括reftitle，refAuthors，refYear，refPublisher （检索模块提供）
13. videoUrl 视频在网上的url，可能为空
14. videoPath 视频的相对路径，可能为空
15. videoContent 包括起始时间startTime 终止时间endTime 视频文字内容textEnglish 对应embedding textEmbedding 和 中文翻译 textChinese （检索模块提供），可能为空
16. codeUrl 代码url，可能为空
17. datasetUrl 数据集url，可能为空
18. cited, 可能为空
## 可以实现的检索功能
1. 可以指定某一个或若干字段针对用户输入的一个query进行检索，支持的字段：
* title
* abstract
* paper_content
* video_content（相当于视频检索）
* authors
2. 可以指定针对论文发表时间的筛选条件
3. 可以指定排序的方式
* year
* relevance
4. 可以为同时检索的不同字段设置不同的检索优先级：例如标题中包含该query的分数比在摘要中包含要分数高。
5. 可以针对某一个单一的视频，返回包含query的视频定位信息（字幕，开始时间，结束时间）
## 视频转换功能
./videoContent
1. videoContent.py       
Input: 视频路径path    
Output: 数据字段"videoContent"
2. 支持mp4,avi,mpg,flv,mov,m4a,3gp等视频格式
## pdf解析功能
./pdfToJson
