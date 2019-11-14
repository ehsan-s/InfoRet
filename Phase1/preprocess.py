import hazm
import nltk
import csv

def read_csv_as_dict():
    with open('../source/English.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(f'\t{row["Title"]} -> {row["Text"]}.')
            line_count += 1
        print(f'Processed {line_count} lines.')


