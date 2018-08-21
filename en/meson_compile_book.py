#!/usr/bin/env python3
import argparse
import os
import sys
import shutil
import subprocess


def concatenate_files(outfile, txtfiles):
    """concatenate_files(outfile, txtfiles) -> None

    Example:
        >>> concatenate_files('all.txt', ['a.txt', 'b.txt'])

    Ref:
        https://stackoverflow.com/a/27077437/5456794

    10MB per writing chunk to avoid reading big file into memory.
    """
    BUFSIZE = 10 << 20
    with open(outfile, 'wb') as outfd:
        for infile in txtfiles:
            with open(infile, 'rb') as infd:
                shutil.copyfileobj(infd, outfd, BUFSIZE)
            outfd.write(b'\n')


def handling_args():
    parser = argparse.ArgumentParser(
        description=(
            "Build html file from asciidoc's docbook backend. "
            "Note: output file in form of book-${lang}.html"
        )
    )
    parser.add_argument(
        'infile',
        help="input file(s) to generate xml file",
        nargs='+'
    )
    parser.add_argument(
        '-l', '--lang',
        help="language pass to asciidoc",
        choices=['en', 'vi'],
        default='en'
    )

    return parser.parse_args()


def main():
    parser = handling_args()

    book_lang = 'book-{}'.format(parser.lang)
    book_lang_txt = '{}.txt'.format(book_lang)
    book_lang_html = '{}.html'.format(book_lang)

    print(">>> Concatenating all .adoc file to {}.".format(book_lang_txt))
    concatenate_files(outfile=book_lang_txt, txtfiles=parser.infile)

    print(">>> Generating .html file from {}.".format(book_lang_txt))
    # Use asciidoc html5 backend to generate output
    asciidoc_args = [
        'asciidoc',
        '-b', 'html5',
        '-a', 'icons',
        '-a', 'toc2',
        '-a', 'theme=flask',
        '-a', 'lang={}'.format(parser.lang),
        '-a', 'numbered',
        '-o', book_lang_html,
        book_lang_txt
    ]

    print("Running command: {}".format(' '.join(asciidoc_args)))

    completed_process = subprocess.run([
        *asciidoc_args,
    ])

    sys.exit(completed_process.returncode)

if __name__ == '__main__':
    main()
