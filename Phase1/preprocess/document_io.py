import csv


def read_csv_file_as_list():
    file_path = '../source/English.csv'
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
