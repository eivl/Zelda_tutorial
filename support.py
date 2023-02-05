from csv import reader


def import_csv_layout(path):
    with open(path) as file:
        return [row for row in reader(file, delimiter=',')]
