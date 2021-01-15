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

ElasticSearch数据库中，一篇文献的存储字段如下：

```json
{
    
}
```

### 字段含义

| 主要字段 | 类型 | 说明 |
| :------: | :--: | :--: |
|          |      |      |
|          |      |      |
|          |      |      |
|          |      |      |
|          |      |      |
|          |      |      |
|          |      |      |
|          |      |      |
|          |      |      |

//xjw



## 功能概要

### 检索

|    功能    | 函数名 | 输入 | 输出 |
| :--------: | :----: | :--: | :--: |
| 按标题检索 |        |      |      |
|            |        |      |      |

// hyx cwh lyw



### pdf抽取

//xjw

//介绍一下实现的功能，重要函数的接口，以便于展示时对照代码讲解



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
