# 将markdown里面的描述数据库的表格代码转换为sql建表语句
# 字段名，字段类型，注释都要自动处理


# 清理好，并切割好每行markdown代码中的各变量
def clean_split_line(line):
    line_clean = line.replace(" ", "")
    line_clean = line_clean.replace("\n", "")
    line_clean = line_clean.replace("\r", "")

    line_clean = line_clean.replace("\\|", "@$@")  # 用一些字段名不用用到的字符先暂时替换所有字符\|,\|是为了防止|被识别
    strings = line_clean.split("|")

    # 把@$@替换回来\|
    strings_append = []
    for string in strings:
        string = string.replace("@$@", "|")
        strings_append.append(string)
    strings = strings_append
    return strings


# 控制区
f = open('markdown_example', encoding='utf-8')
table_name = 'POI'
primary_key = "id"
is_primary_key_auto_increment = 1
table_comment = "POI节点数据"

if is_primary_key_auto_increment:
    auto_increment_word = 'auto_increment '
else:
    auto_increment_word = ''
print("CREATE TABLE `{table}` (".format(table=table_name))
for line in f.readlines():
    strings = clean_split_line(line)
    database_field_name = strings[0]
    json_field_name = strings[1]
    meaning = strings[2]
    database_field_type = strings[3]
    preprocessing = strings[5]
    allow_null = strings[7]
    if int(allow_null):
        allow_null_word = 'DEFAULT'
    else:
        allow_null_word = 'NOT'
    if database_field_name == primary_key:  # 主键
        print(
            "    `{database_field_name}` {database_field_type} NOT NULL {auto_increment_word}COMMENT '{meaning}',".format(
                database_field_name=database_field_name,
                database_field_type=database_field_type,
                auto_increment_word=auto_increment_word,
                meaning=meaning
            )
        )
    else:
        print("    `{database_field_name}` {database_field_type} {allow_null_word} NULL COMMENT '{meaning}',".format(
            database_field_name=database_field_name,
            database_field_type=database_field_type,
            meaning=meaning,
            allow_null_word=allow_null_word
        )
        )
print("    PRIMARY KEY (`{primary_key}`)".format(primary_key=primary_key))
print(") ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_BIN COMMENT='{table_comment}';".format(
    table_comment=table_comment
)
)
