# -*- coding:utf-8 -*-
import sys
import re
import json
reload(sys)
sys.setdefaultencoding('utf-8')

class TemporalProperty():
    """
    从CN-DBpedia的三元组中整理出与时间相关的属性与属性值
    """
    @classmethod
    def list_candidate_property(cls):
        """
        根据先关字找出可能与时间相关的属性名称列表
        :return:
        """
        hot_char_list = ["时", "日", "周", "星期", "月",
                         "季", "节", "年", "朝代", "公元",
                         "天干", "地支", "干支", "甲子", "世纪", "期"]

        candidate_dict = {}  # 候选属性字典,顺便也记录一下各候选属性频次
        with open("../data_file/baike_triples.txt", 'r') as in_file:
            for line in in_file.readlines():
                try:
                    property_key = line.split()[1].strip()
                    for hot_char in hot_char_list:
                        if hot_char in property_key:
                            if candidate_dict.get(property_key):
                                candidate_dict[property_key] += 1
                            else:
                                candidate_dict[property_key] = 1
                                print property_key
                            break
                except Exception, e:
                    print e

        # 存一份json方便加载
        with open("../data_file/candidate_property.json", 'w') as out_file:
            json.dump(candidate_dict, out_file)
        # 存一份txt方便人工筛选
        with open("../data_file/candidate_property.txt", 'a') as out_file:
            for key in candidate_dict:
                out_file.write(key+"\n")
        print len(candidate_dict)


    @classmethod
    def candidate_property_top_all(cls):
        """
        按频次排序,取候选属性中
        :return:
        """
        with open("../data_file/candidate_property.json", 'r') as in_file:
            property_dict = json.load(in_file)

        with open("../data_file/candidate_property_top_all.txt", 'a') as out_file:
            for item in sorted(property_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True):
                print item[0], item[1]
                out_file.write(str(item[0])+"\t"+str(item[1])+"\n")

    @classmethod
    def split_top_all(cls):
        """
        将大部分带时间,日期,年份,年代的与其他杂乱属性分开
        :return:
        """
        with open("../data_file/candidate_property_top_all.txt", 'r') as in_file:
            for line in in_file.readlines():
                if "时间" in line or "日期" in line or "年份" in line or "年代" in line or "月份" in line or "时长" in line or '所处时代' in line:
                    with open("../data_file/clean_candidate_property.txt", 'a') as out_file:
                        out_file.write(line)
                else:
                    with open("../data_file/dirty_candidate_property.txt", 'a') as out_file:
                        out_file.write(line)


    @classmethod
    def temporal_triple_filter(cls):
        """
        根据top_1000时间属性内容,筛选出时间相关三元组,属性值即为时间表达式
        :return:
        """

        top_1000_dict = {}
        with open("../data_file/clean_candidate_property.txt", 'r') as in_file:
            for line in in_file.readlines():
                top_1000_dict[line.split()[0]] = int(line.split()[1].strip())

        out_file = open("../data_file/temporal_triples.txt", 'a')
        with open("../data_file/baike_triples.txt", 'r') as in_file:
            for line in in_file.readlines():
                property_key = line.split()[1]
                if top_1000_dict.get(property_key):
                    out_file.write(line)

        out_file.close()

    @classmethod
    def temporal_expression(cls):
        """
        整理出时间属性的属性值
        :return:
        """
        out_file = open("../data_file/temporal_expression.txt", 'a')
        no_digit_file = open("../data_file/temporal_expression_no_digit.txt", 'a')
        count = 0
        no_digit_count = 0
        with open("../data_file/temporal_triples.txt", 'r') as in_file:
            for line in in_file.readlines():
                if "未知" not in line and "出版社" not in line.split()[-1] and len(line.split()[-1])<20:
                    out_file.write(line.split()[-1].strip().replace("<a>", '').replace("</a>", '')+"\n")
                    if not any(char.isdigit() for char in line.split()[-1]):
                        no_digit_file.write(line.split()[-1].strip().replace("<a>", '').replace("</a>", '')+"\n")
                        no_digit_count += 1
                count += 1
        print "count:", count
        print "no_digit:", no_digit_count


    @classmethod
    def temporal_expression_deduplicate(cls):
        """
        时间表达式去重
        :return:
        """
        temporal_expression_dict = {}
        with open("../data_file/temporal_expression.txt", 'r') as in_file:
            for line in in_file:
                if temporal_expression_dict.get(line.strip()):
                    temporal_expression_dict[line.strip()] += 1
                else:
                    temporal_expression_dict[line.strip()] = 1
        with open("../data_file/temporal_expression_deduplicate.txt", 'a') as out_file:
            for item in sorted(temporal_expression_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True):
                out_file.write(item[0]+"\t"+str(item[1])+"\n")

        print "deduplicate:", len(temporal_expression_dict)



        # 无数字的表达式
        no_digit_dict = {}
        with open("../data_file/temporal_expression_no_digit.txt", 'r') as in_file:
            for line in in_file:
                if no_digit_dict.get(line.strip()):
                    no_digit_dict[line.strip()] += 1
                else:
                    no_digit_dict[line.strip()] = 1
        with open("../data_file/temporal_expression_no_digit_deduplicate.txt", 'a') as out_file:
            for item in sorted(no_digit_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True):
                out_file.write(item[0]+"\t"+str(item[1])+"\n")
        print "deduplicate no digit:", len(no_digit_dict)






# TemporalProperty.list_candidate_property()
# TemporalProperty.candidate_property_top_all()
# TemporalProperty.split_top_all()

# TemporalProperty.temporal_triple_filter()
# TemporalProperty.temporal_expression()
# TemporalProperty.temporal_expression_deduplicate()







