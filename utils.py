import re
from collections import Counter


def clean_text(text: str):
    text = text.lower().replace("\n", " ").replace(".", " ")
    text = re.sub(r"[^a-z ]", "", text)
    return text


def get_word_occurences(text: str):
    words = text.split(" ")
    word_occurences = {}
    for word in words:
        if word == "":
            continue
        if word in word_occurences:
            word_occurences[word] += 1
        else:
            word_occurences[word] = 1
    return word_occurences


def combine_word_occurences(first: dict, second: dict):
    return dict(Counter(first) + Counter(second))
