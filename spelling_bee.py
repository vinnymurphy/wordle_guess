#!/usr/bin/env python

# -*- mode: Python; python-indent: 4; -*-
# vim: tabstop=8 expandtab sw=4 softtabstop=4 ai sm

"""File:    spelling_bee.py
Author:  Vinny Murphy
Created: 12Jun23

* Words must contain at least 4 letters.
* Words must include the center letter.
* Our word list does not include words that are obscure, hyphenated,
  or proper nouns.
* No cussing either, sorry.
* Letters can be used more than once.

* Score points to increase your rating.
* 4-letter words are worth 1 point each.
* Longer words earn 1 point per letter.
* Each puzzle includes at least one “pangram” which uses every
  letter. These are worth 7 extra points!

"""
from __future__ import print_function

import argparse
from itertools import combinations
from pathlib import Path


def parse_args():
    """Create command line parser
    :return: the arguments
    :rtype: parser.parse_args()
    """
    desc = __import__("__main__").__doc__
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=desc
    )
    parser.add_argument("-m", "--musthave", help="letter we must have")
    parser.add_argument(
        "-l", "--letters", help="letters we can use", type=list
    )
    return parser.parse_args()


def get_combinations(must_have, letters):
    """
    We will get the combinations of the letters in order to get a better
    guess at spelling bee.  The must_have is the letter in the middle that
    needs to be in all the words.  The letters don't have to be in the word
    and can be repeated.

    Parameters
    ----------
    must_have -> set
    letters -> set

    Returns
    -------
    return list of letter combinations

    """
    needed_letters = []
    for i in reversed(range(3, 8)):
        needed_letters.extend(
            set(x).union(must_have) for x in (combinations(letters, i))
        )
    return needed_letters


def main():
    """ "
    get the list of words that we want to try

    """
    args = parse_args()
    dictionary = "./words_alpha.text"
    words = [
        word.lower().strip()
        for word in Path(dictionary).read_text().splitlines()
        if 7 >= len(word) > 3 and args.musthave in set(word)
    ]
    combos = get_combinations(args.musthave, args.letters)
    guess = set()
    for combo in combos:
        guess.update(w for w in words if set(w) == combo)
    print("\n".join(sorted(guess, key=len, reverse=True)[:40]))


if __name__ == "__main__":
    main()
