#!/usr/bin/env python

# -*- mode: Python; python-indent: 4; -*-
# vim: tabstop=8 expandtab sw=4 softtabstop=4 ai sm

"""File:     wordle.py
Author:   Vinny Murphy
Created:  Sunday 2022/03/13

Some code taken from https://www.inspiredpython.com/article/
                     solving-wordle-puzzles-with-basic-python

We look at all the words in the dictionary and determine what letters
are the most used.  An issue with using the words from the unix is
they are not the words used by NY Times.

Another issue with just looking at the letters we can not determine
what words are used the most.  Once we get down to a managable set of
words we sort by how often a word is using ./big.txt

big.txt comes from the Natural Language Corpus Data.  I'm not
convinced this is the best probability of words, but it is a perfect
approximation of words in the English language.

https://norvig.com/ngrams/

"""


import argparse
import contextlib
import operator
import re
import string
import sys
from collections import Counter, defaultdict
from itertools import chain
from pathlib import Path

ALLOWABLE_CHARACTERS = set(string.ascii_letters)
ALLOWED_ATTEMPTS = 6
WORD_LENGTH = 5


def calculate_word_commonality(word: str) -> float:
    """Calculate word commonality.

    we need to take our letter frequency table and make a word scoring
    function that scores how “common” the letters are in that word
    """
    score = 0.0
    for char in word:
        score += LETTER_FREQUENCY[char]
    return score / (WORD_LENGTH - len(set(word)) + 1)


def sort_by_word_commonality(words: list) -> list:
    """sort by word commonality"""
    if len(words) < 30:
        sort_by = operator.itemgetter(2, 1)
    else:
        sort_by = operator.itemgetter(1, 2)
        #    (word, calculate_word_commonality(word), 0.0)
    return sorted(
        [
            (
                word,
                calculate_word_commonality(word),
                probability_count(word, COUNT_WORDS),
            )
            for word in words
        ],
        key=sort_by,
        reverse=True,
    )


def display_word_table(word_commonalities):
    """discplay word table

    generate a sorted (highest-to-lowest) list of tuples, with each tuple
    containing the word and the calculated score for that word. The sorting
    key is the score."""
    for (word, freq, probility) in word_commonalities:
        print(f"{word:<10} | {freq:<5.2} | {probility:<.4E}")


def input_word():
    """Input word"""
    while True:
        try:
            word = input("Input the word you entered> ")
        except KeyboardInterrupt:
            print("C YA!")
            sys.exit()
        if len(word) == WORD_LENGTH and word.lower() in WORDS:
            break
    return word.lower()


def input_response() -> str:
    """Get the response or G, Y or ?

    ask the user for a WORD_LENGTH word they gave Wordle, and I want to record
    the response from Wordle. As there is only three possible answers
    (green, yellow, and gray) I encode it as a simple string of three
    characters: G, Y, and ?."""
    print("Type the color-coded reply from Wordle:")
    print("  G for Green")
    print("  Y for Yellow")
    print("  ? for Gray")
    while True:
        response = input("Response from Wordle> ")
        if len(response) == WORD_LENGTH and set(response.upper()) <= {
            "G",
            "Y",
            "?",
        }:
            break
        print(f"Error - invalid answer {response}")
    return response.upper()


def green_choices(words, green):
    """Any choices that are green should be included at that location.

    green is a dictionary of letters and exact locations.

    """
    for letter in green:
        for location in green[letter]:
            here_i_am = int(location)
            new_words = [w for w in words if w[here_i_am] == letter]
    return new_words


def yellow_choices(words, yellow):
    """Any choices that are green should be excluded from that
    location

    yellow is a dictionary of letters and inexact locations.

    """
    for letter in yellow:
        for location in yellow[letter]:
            here_i_am = int(location)
            new_words = [w for w in words if w[here_i_am] != letter]
    return new_words


def exclude_these_words(words, exclusions, inclusions):
    """Words can have anything in the exclusion list"""
    words = [w for w in words if set(inclusions).issubset(w)]
    exclude_re = re.compile(r"|".join(exclusions))
    return [w for w in words if not exclude_re.search(w)]


def match(possible_words, green_yellow):
    """green_yellow contains the dictionary of where the yellows didn't match and
    the greens did match.
    """
    words = possible_words.copy()
    excludes = list(green_yellow["?"].keys())
    green_keys = list(green_yellow["G"].keys())
    yellow_keys = list(green_yellow["Y"].keys())
    includes = green_keys + yellow_keys
    words = exclude_these_words(words, excludes, includes)

    if yellow := green_yellow["Y"]:
        words = yellow_choices(words, yellow)

    if green := green_yellow["G"]:
        words = green_choices(words, green)

    return words


def solve():
    """solve the word"""
    possible_words = WORDS.copy()
    all_green = "G" * WORD_LENGTH
    word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]

    response_dict = {
        "?": defaultdict(set),
        "G": defaultdict(set),
        "Y": defaultdict(set),
    }

    for attempt in range(1, ALLOWED_ATTEMPTS + 1):
        print(f"Attempt {attempt} with {len(possible_words)} possible words")
        display_word_table(sort_by_word_commonality(possible_words)[:15])
        word = input_word()
        response = input_response()
        if response == all_green:
            print(f'Congrats! The word "{word}" is correct', end=" ")
            print(f"after {attempt} attempt{'s'[:attempt ^ 1]}.")
            break
        for choice, letter in zip(response, word):
            response_dict[choice][letter].add(word.index(letter))
        for location, letter in enumerate(response):
            if letter == "?":
                for vector in word_vector:
                    with contextlib.suppress(KeyError):
                        vector.remove(word[location])
            elif letter == "G":
                word_vector[location] = {word[location]}
            elif letter == "Y":
                with contextlib.suppress(KeyError):
                    word_vector[location].remove(word[location])
        past = possible_words.copy()
        possible_words = match(possible_words, response_dict)

        if not possible_words:
            possible_words = past
            possible_words.remove(word)


def parse_args():
    """Create command line parser
    :return: the arguments
    :rtype: parser.parse_args()
    """
    desc = __import__("__main__").__doc__
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=desc
    )
    return parser.parse_args()


def trim_to_size(word_list):
    """Trim the word list down to only length of WORD_LENGTHH and only has
    allowable characters."""
    return {
        word.lower()
        for word in filter(
            lambda w: len(w) == WORD_LENGTH and set(w) < ALLOWABLE_CHARACTERS,
            word_list,
        )
    }


def get_words():
    """Get the words from a file"""
    dictionary = "/usr/share/dict/words"
    # pylint: disable=unspecified-encoding
    return trim_to_size(Path(dictionary).read_text().splitlines())


def big_words(text):
    """from the corpus get all the five-letter words"""
    return re.findall(r"\w{5}", text.lower())


def probability_count(word, count_words):
    """Get the sum of the words and divide it by the count of the words"""
    count = sum(count_words.values())
    return count_words[word] / count


if __name__ == "__main__":
    args = parse_args()
    WORDS = get_words()
    with open("./big.txt", encoding="utf-8") as reader:
        big_list = [
            word for word in big_words(reader.read()) if word in WORDS
        ]
        COUNT_WORDS = Counter(big_list)
    LETTER_COUNTER = Counter(chain.from_iterable(WORDS))
    LETTER_FREQUENCY = {
        character: value / sum(LETTER_COUNTER.values())
        for character, value in LETTER_COUNTER.items()
    }
    solve()
