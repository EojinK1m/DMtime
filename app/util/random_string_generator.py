import random
import re

code_characters = [
    "Q",
    "W",
    "E",
    "R",
    "T",
    "Y",
    "U",
    "I",
    "O",
    "P",
    "A",
    "S",
    "D",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "Z",
    "X",
    "C",
    "V",
    "B",
    "N",
    "M",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]

RANDOM_TOKEN_LENGTH = 10


def validate_verification_code(code):
    if not isinstance(code, str):
        raise TypeError("code is not string")

    p = re.compile("[0-9A-Z]{10}")
    return p.match(code) != None


def generate_random_string(length):
    random.shuffle(code_characters)
    code_list = code_characters[0:length]
    return "".join(code_list)


def generate_verification_code():
    return generate_random_string(RANDOM_TOKEN_LENGTH)