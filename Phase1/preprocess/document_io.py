import csv
import xml.etree.ElementTree as ET


def read_csv_file_as_list():
    file_path = '../../source/English.csv'
    eng_list = []
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            # print(f'\t{row["Title"]} -> {row["Text"]}.')
            line_count += 1
            eng_list.append((row["Title"], row["Text"]))
        # print(f'Processed {line_count} lines.')
        return eng_list


def read_persian_xml_file_as_list():
    tree = ET.parse('../../source/Persian.xml')
    root = tree.getroot()
    prefix_element_name = "{http://www.mediawiki.org/xml/export-0.10/}"
    per_list = []
    for page in root:
        title = page.find(prefix_element_name + 'title').text
        text = page.find(prefix_element_name + 'revision').find(prefix_element_name + 'text').text
        per_list.append((title, text))
    return per_list
