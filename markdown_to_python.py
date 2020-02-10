"""
将markdown里面的描述数据库的表格代码转换为python解析接口代码
"""


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


def preprocessing_identify(database_field_type):
    preprocessing_string = 'safe_str()'
    if database_field_type == 'int':
        preprocessing_string = 'safe_int()'
    elif database_field_type == 'float':
        preprocessing_string = 'safe_float()'
    elif database_field_type == 'datetime':
        preprocessing_string = 'safe_datetime()'
    elif database_field_type == 'date':
        preprocessing_string = 'safe_date()'
    elif database_field_type == 'time':
        preprocessing_string = 'safe_time()'
    return preprocessing_string


f = open('markdown_example', encoding='utf-8')
json_name = "POI"  # 要解析的json在你的代码中定义的名字
separation_character = '-'  # 用于分割字段与子字段的字符

for line in f.readlines():
    strings = clean_split_line(line)
    database_field_name = strings[0]
    json_field_name = strings[1]
    database_field_type = strings[3]
    preprocessing = preprocessing_identify(database_field_type)

    if database_field_name == 'snapshot_time':
        print("'snapshot_time': datetime.utcnow()")
    else:
        json_field_name_split = json_field_name.split(separation_character)
        answer = "'{database_field_name}': self.{preprocessing}({json_name}".format(
            database_field_name=database_field_name,
            preprocessing=preprocessing.strip(')'),
            json_name=json_name
        )
        for i in range(len(json_field_name_split) - 1):
            string = ".get('{field_value}', {empty_dict})".format(field_value=json_field_name_split[i], empty_dict='{}')
            answer = answer + string
        answer = answer + ".get('{field_value}', None))".format(field_value=json_field_name_split[-1])
        print(answer)
