# spider_helper

Use the json from ajax response to automatically create:
1. A web scraping documentation
2. Python analysis code of the json.
3. SQL CREATE TABLE Statement which creates a table to store data from the json.

爬虫编写小工具(接口json转markdown爬虫文档表格代码，转解析接口json的python代码，转数据库建表语句)

接口json，爬虫文档markdown中描述数据库的表格代码，和解析接口json的python代码，以及数据库建表语句有许多重复部分，可以用代码自动转换，更容易同步修改避免错误

使用步骤
1. json_to_markdown.py将接口json转换为爬虫文档markdown的表格代码
2. 根据多次请求返回总结，修改爬虫文档markdown的表格代码
3. markdown_to_python.py将爬虫文档markdown的表格代码转化为python解析接口字段代码
4. markdown_to_mysql.py将爬虫文档markdown的表格代码转化生成mysql建表代码

更新
1. '预处理'字段删除了，因为确定了类型就肯定要进行对应预处理以防万一
