from main.models import SchemasColumn, DataSets
from django.core.files import File
from os import remove

from .small_generators import *
import csv


def generate_file(dataset_id):
    """Generating .csv file from schema to user directory"""
    dataset = DataSets.objects.get(id=dataset_id)
    column_separator = dataset.schema.column_separator
    string_character = dataset.schema.string_character
    rows_amount = dataset.rows
    row_list = []

    column_set = SchemasColumn.objects.filter(schema=dataset.schema).order_by("order")

    row_list.append([obj.name for obj in column_set])
    pattern = generate_column_pattern(column_set)

    for i in range(rows_amount):
        row_list.append(generate_row_from_pattern(pattern))

    filename = f"CSV_{dataset.date_created.strftime('%Y-%m-%d %H:%M:%S')}.csv"

    with open(filename, "w", newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=column_separator, quotechar=string_character)
        writer.writerows(row_list)

    dataset.file.save(filename, File(open(filename, "rb")))
    dataset.ready = True
    dataset.save()

    remove(filename)

def generate_column_pattern(column_set):
    """
    Generating pattern for future parsing and row generation
    Example pattern: [["F"],["P"],["I", 10, 23],["T", 2]]
    """
    pattern = []
    for column in column_set:
        category = column.category
        if category == "full_name":
            pattern.append(["F"])
        elif category == "email":
            pattern.append(["E"])
        elif category == "phone_number":
            pattern.append(["P"])
        elif category == "integer":
            pattern.append(["I", column.min_integer, column.max_integer])
        else:
            # T is for total sentences
            pattern.append(["T", column.sentence_amount])

    return pattern

def generate_row_from_pattern(pattern):
    """Generating data row from pattern by using small generators"""
    row = []
    for element in pattern:
        symbol = element[0]
        if symbol == "F":
            row.append(gen_fullname())
        elif symbol == "E":
            row.append(gen_email())
        elif symbol == "P":
            row.append(gen_phone_number())
        elif symbol == "I":
            row.append(gen_integer(element[1], element[2]))
        else:
            row.append(gen_text(element[1]))
    return row
