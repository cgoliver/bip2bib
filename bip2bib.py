import os
import sys
import argparse
import random

import pythonbible as bible


def cline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--seed", default=3, type=int, help="Random seed for reproducibility.")
    parser.add_argument(
        "-o",
        "--outfile",
        default="mapping.txt",
        type=str,
        help="Path to output file where mapping is stored. Default: ./mapping.txt",
    )
    return parser.parse_args()
    pass


def load_bip39():
    return [word.strip() for word in open("english.txt").readlines()]


def dump_bible():
    verselist = []
    with open("verses.txt", "w") as bib:
        all_books = bible.Book
        for book in all_books:
            if book.value > 66:
                break
            num_chapters = bible.get_number_of_chapters(book)
            for chapter in range(1, num_chapters + 1):
                num_verses = bible.get_number_of_verses(book, chapter)
                for verse in range(1, num_verses + 1):
                    verse_id = bible.get_verse_id(book, chapter, verse)
                    ref = bible.convert_verse_ids_to_references([verse_id])
                    name = bible.format_scripture_references(ref)
                    bib.write(f"{name}\n")


def build_index(args) -> str:
    if not os.path.exists("verses.txt"):
        print(
            "DANGER: Writing verse list to verses.txt. If this is not your first time building a mapping, make sure this verse list is identical to the one you used to first create your mapping. It is best to always use the one already provided in this repository."
        )
        dump_bible()
    verses = [verse.strip() for verse in open("verses.txt", "r").readlines()]
    random.seed(args.seed)
    random.shuffle(verses)
    wordlist = load_bip39()
    with open(args.outfile, "w") as outf:
        for i, word in enumerate(wordlist):
            outf.write(f"{word} {verses[i]}\n")


if __name__ == "__main__":
    print("WARNING: To ensure mapping is reproducible, make sure you are always using the same Python version")
    args = cline()
    build_index(args)
    pass
