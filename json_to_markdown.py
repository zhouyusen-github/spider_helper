# 接口数据直接转化为markdown数据
# varchar长度后期要改，因为数据多了，奇怪的情况就会出现

import json
import datetime


# 分析字段内容类型，填入markdown中'数据库字段类型'，'预处理'位置
def type_indentify(value):
    answer = {'type': ''}
    value_type = type(value)
    if value_type != str:
        if value_type == int:
            answer['type'] = 'int'
        elif value_type == float:
            answer['type'] = 'float'
        elif value_type == list:
            if len(value) == 0:  # 应付[]这种异常
                answer['type'] = 'varchar(40)'
            else:
                answer['type'] = 'varchar({length})'.format(length=str(len(str(value))))
        elif value_type == dict:
            answer['type'] = 'dict'  # 有子字段另外处理
    elif value_type == str:
        try:
            int(value)
            if int(value[0]) != 0:  # 排除int('010200')
                answer['type'] = 'int'
            else:
                answer['type'] = 'varchar({length})'.format(length=str(len(str(value))))
        except:
            try:  # 先int再float，因为float可以转化int的字符串的，反之不行
                float(value)
                answer['type'] = 'float'
            except:
                try:
                    datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                    answer['type'] = 'datetime'
                except:
                    try:
                        datetime.datetime.strptime(value, "%Y-%m-%d")
                        answer['type'] = 'date'
                    except:
                        try:
                            datetime.datetime.strptime(value, "%H:%M:%S")
                            answer['type'] = 'time'
                        except:
                            answer['type'] = 'varchar({length})'.format(length=str(len(str(value))))
    return answer


def print_markdown(json_dict, father_key=None):  # 输出markdown表格文件
    for key in json_dict:
        if isinstance(json_dict[key], str):
            value = json_dict[key].replace("|", "\|")
        else:
            value = json_dict[key]
        answer = type_indentify(value)
        value_type = answer['type']
        if father_key:
            key = father_key + '-' + key
        print("--- | {key} | --- | {type} | {value} || ".format(key=key,
                                                                type=value_type,
                                                                value=value,
                                                                ))
        if value_type == 'dict':  # 如果有子字段也要解析
            print_markdown(value, key)


f = open('json_example', encoding='utf-8')
json_string = f.read()
json_dict = json.loads(json_string)
print('数据库字段名 | 接口字段名 | 意义 | 数据库字段类型 | 例子 | 异常返回| 不可为null')
print('---|---|---|---|---|---|---')
print_markdown(json_dict)
print("snapshot_time | --- | --- | datetime | --- |")
