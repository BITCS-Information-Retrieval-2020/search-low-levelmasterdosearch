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
15. videoContent 包括起始时间列表StartTime 终止时间列表EndTime 和视频文字内容列表 videoText （检索模块提供），可能为空
16. codeUrl 代码url，可能为空
17. datasetUrl 数据集url，可能为空
