from names import get_full_name
from essential_generators import DocumentGenerator
from random import randint


gen = DocumentGenerator()

def gen_fullname():
    return get_full_name()

def gen_email():
    return gen.email()

def gen_phone_number():
    range_start = 10 ** (9 - 1)
    range_end = (10 ** 9) - 1
    return f"+380{randint(range_start, range_end)}"

def gen_integer(min_value, max_value):
    return randint(min_value, max_value)

def gen_text(amount):
    """Generating sentence with 5 words N times and combining it to one big sentence"""
    return " ".join([gen.gen_sentence(5, 5) for word in range(amount)])
