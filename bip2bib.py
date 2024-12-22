import os
import sys
import argparse
import hashlib

import pythonbible as bible


def cline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--passphrase",
        default="",
        type=str,
        help="Optional string appended to word index before hashing, acts as passphrase.",
    )
    parser.add_argument(
        "-o", "--outfile", default="mapping.txt", type=str, help="Path to output file where mapping is stored."
    )
    return parser.parse_args()
    pass


def idx_hash(num, secret="", mod=2048):
    """
    Hash an integer, modulo by a value, and map to an integer.

    :param num: The integer to hash.
    :param mod: The modulo value (default is 2048).
    :return: An integer in the range [0, mod-1].
    """
    # Convert the integer to bytes
    num_bytes = f"{num}{secret}".encode("utf-8")

    # Create a hash (using SHA-256 as an example)
    hashed = hashlib.sha256(num_bytes).hexdigest()

    # Convert the hash to an integer and take modulo
    result = int(hashed, 16) % mod
    return result


def load_bip39():
    return [word.strip() for word in open("english.txt").readlines()]


def dump_bible():
    verselist = []
    with open("verses.txt", "w") as bib:
        all_books = bible.Book
        for book in all_books:
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
    wordlist = load_bip39()
    with open(args.outfile, "w") as outf:
        for idx, word in enumerate(wordlist):
            new_idx = idx_hash(idx, secret=args.passphrase, mod=len(verses))
            outf.write(f"{word} {verses[new_idx]}\n")


if __name__ == "__main__":
    args = cline()
    build_index(args)
    pass
