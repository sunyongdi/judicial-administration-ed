"""
该文件主要的作用是存储一些我们要用到的数据
"""
import os
import json
from collections import defaultdict

data_path = './data/law_data'
kb_data_file = data_path + '/kb.json'
train_data_file = data_path + '/train.json'

# 保存知识库中所有的别名以及实体，格式为每个名字一行
# 我们也将训练集中的提及加入到这里面，因为像南京南站虽然是知识库中的提及，但是在知识库中并没有该实体名
# 将所有的英文全部转换为小写
alias_and_subjects = []
alias_and_subjects_file = open(data_path+'/alias_and_subjects.txt','w',encoding='utf-8')
# 保存每个实体在知识库中对应的id（一对多），
# 格式为名字：{'subject_id':'','subject_name':''}
entity_to_ids = defaultdict(list)
entity_to_ids_files = open(data_path+'/entity_to_ids.json','w')
# 用于保存每个实体的类型
entity_type = []
entity_type_file = open(data_path+'/entity_type.txt','w',encoding='utf-8')
# 用于保存每个subject_id对应的信息
subject_id_with_info = defaultdict(dict)
subject_id_with_info_file = open(data_path+'/subject_id_with_info.json','w')

with open(kb_data_file,'r') as fp:
    lines = fp.readlines()
    total = len(lines)-1
    for i,line in enumerate(lines):
        print(i, total)
        line = eval(line)
        for e_type in line['type']:
            entity_type.append(e_type)
        for word in line['alias']:
            word = word.lower()
            alias_and_subjects.append(word)
            if line['subject_id'] not in entity_to_ids[word]:
                entity_to_ids[word].append(line['subject_id'])
        subject_id_with_info[line['subject_id']] = line

print("===============================")
with open(train_data_file,'r') as fp:
    lines = fp.readlines()
    total = len(lines)-1
    for i,line in enumerate(lines):
        print(i, total)
        line = eval(line)
        mention_datas = line['mention_data']
        for mention_data in mention_datas:
            word = mention_data['mention'].lower()
            alias_and_subjects.append(word)
            if mention_data['kb_id'] not in entity_to_ids[word]:
                entity_to_ids[word].append(mention_data['kb_id'])

entity_type = list(set(entity_type))
entity_type_str = "\n".join(entity_type)
alias_and_subjects = sorted(list(set(alias_and_subjects)), key=lambda x: len(x), reverse=True)
alias_and_subjects_str = "\n".join(alias_and_subjects)

alias_and_subjects_file.write(alias_and_subjects_str)
entity_type_file.write(entity_type_str)
entity_to_ids_files.write(json.dumps(entity_to_ids, ensure_ascii=False))
subject_id_with_info_file.write(json.dumps(subject_id_with_info, ensure_ascii=False))

alias_and_subjects_file.close()
entity_type_file.close()
entity_to_ids_files.close()
subject_id_with_info_file.close()
