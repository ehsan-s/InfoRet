import csv
import xml.etree.ElementTree as ET
import re


def read_csv_file(addr='source/phase2_train.csv'):
    file_path = addr
    text_list = []
    tag_list = []
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            line_count += 1
            title = re.sub(' +', ' ', row["Title"].strip())
            text = re.sub(' +', ' ', row["Text"].strip())
            tag_list.append(int(row["Tag"]))
            text_list.append(title + ' ' + text)
        return {'text': text_list, 'tag': tag_list}
