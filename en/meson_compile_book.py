#!/usr/bin/env python3
import argparse
import os
import sys
import shutil
import subprocess
import string


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
        for filename in txtfiles:
            with open(filename, 'rb') as infile:
                shutil.copyfileobj(infile, outfd, BUFSIZE)


def handling_args():
    parser = argparse.ArgumentParser(description="Build xml file from asciidoc's docbook backend.")
    parser.add_argument('infile',
                        help="input file(s) to generate xml file",
                        nargs='+')
    parser.add_argument('-l', '--lang',
                        help="language pass to asciidoc, either `en' or `vi'",
                        default='en')
    parser.add_argument('-o', '--out',
                        help="output filename (usually based on language)",
                        default='book-en.xml')

    return parser.parse_args()


def main():
    parser = handling_args()

    filename, ext = os.path.splitext(parser.out)
    book_all_txt = ''.join([filename, 'txt'])

    concatenate_files(outfile=book_all_txt, txtfiles=parser.infile)

    subprocess.call(['asciidoc',
                    '-a', ''.join(['lang=', parser.lang]),
                    '-d', 'book',
                    '-b', 'docbook',
                    '-o', parser.out,
                    book_all_txt])


if __name__ == '__main__':
    main()
