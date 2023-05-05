import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor


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


def get_word_occurences_parallel(text: list[str]):
    with ThreadPoolExecutor() as executor:
        word_occurences = executor.map(get_word_occurences, text)

    combined_word_occurences = {}
    for word_occurence in word_occurences:
        combined_word_occurences = combine_word_occurences(
            combined_word_occurences, word_occurence)
    return combined_word_occurences
