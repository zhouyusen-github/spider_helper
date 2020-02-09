# 将markdown里面的描述数据库的表格代码转换为sql建表语句


# 我觉得用python readline好

# 字段名，数据库类型，注释都要自动处理
'''
    def save_string_safely(field):
        if type(field) != str:
            return str(field)
        else:
            return field
'''

f = open('markdown_example', encoding='utf-8')

jsonname = "POI"  # 要解析的json，你在代码中定义的名字
for line in f.readlines():
    line_clean = line.replace(" ", "")
    line_clean = line_clean.replace("\n", "")
    line_clean = line_clean.replace("\|", "@$@")  # 用一些字段名不用用到的字符先暂时替换所有字符\|
    strings = line_clean.split("|")

    # 把@$@替换回来\|
    strings_append = []
    for string in strings:
        string = string.replace("@$@", "|")
        strings_append.append(string)
    strings = strings_append

    # print(strings)

    # print("`{field}` {char} DEFAULT NULL  # {note}".format(field=strings[0], char=strings[3], note=strings[2]))
    database_field_name = strings[0]
    json_field_name = strings[1]
    meaning = strings[2]
    database_field_type = strings[3]
    preprocessing = strings[5]
    allow_null = strings[7]
    if "varchar" in database_field_type:
        database_field_type = 'str'

    field_value_split = json_field_name.split('-')
    if len(field_value_split) == 2:
        answer = "'{field}': self.safe_str({jsonname}.get('{field_value1}', safe_change).get('{field_value2}', None)),".format(field=database_field_name, jsonname=jsonname, field_value1=field_value_split[0], field_value2=field_value_split[1])
        answer = answer.replace('safe_change','{}')
        print(answer)

    else:
        if database_field_name != 'snapshot_time':
            print("'{field}': self.safe_str({jsonname}.get('{field_value}', None)),".format(field=database_field_name, jsonname=jsonname,
                                                                                            field_value=json_field_name))
        else:
            print("'snapshot_time': datetime.utcnow()")
