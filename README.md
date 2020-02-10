# spider_helper
爬虫编写小工具(markdown文档表格代码，转解析返回json的python代码，转数据库建表语句)

爬虫文档中描述数据库的表格代码，和解析接口json，以及数据库建表语句有许多重复部分，可以用代码自动转换，更容易同步修改避免错误

使用步骤
1. json_to_markdown将接口json转换为markdown
2. 根据多次请求返回总结，修改markdown
3. markdown_to_python生成python解析接口字段代码
4. markdown_to_mysql生成mysql建表代码

更新
1.预处理字段删除了，因为确定了类型就肯定要进行对应预处理以防万一