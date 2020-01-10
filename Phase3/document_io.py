import csv
import re


def read_csv_file(addr='source/Data.csv'):
    file_path = addr
    text_list = []
    id_list = []
    with open(file_path, mode='r', encoding='latin-1') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            line_count += 1
            text = re.sub(' +', ' ', row["Text"].strip())
            id_list.append(int(row["ID"]))
            text_list.append(text)
        return {'text': text_list, 'id': id_list}


def write_csv_file(file_path, id_list, label_list):
    with open(file_path, mode='w') as clustering_file:
        writer = csv.writer(clustering_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(id_list)):
           writer.writerow([id_list[i], label_list[i]])
