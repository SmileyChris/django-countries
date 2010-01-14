#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
titlecase.py v0.3
Original Perl version by: John Gruber http://daringfireball.net/ 10 May 2008
Python version by Stuart Colville http://muffinresearch.co.uk
License: http://www.opensource.org/licenses/mit-license.php
"""

import sys
import re

__all__ = ['titlecase']


SMALL = 'a|an|and|as|at|but|by|en|for|if|in|of|on|or|the|to|v\.?|via|vs\.?'
PUNCT = "[!\"#$%&'‘()*+,-./:;?@[\\\\\\]_`{|}~]"

SMALL_WORDS = re.compile(r'^(%s)$' % SMALL, re.I)
INLINE_PERIOD = re.compile(r'[a-zA-Z][.][a-zA-Z]')
UC_ELSEWHERE = re.compile(r'%s*?[a-zA-Z]+[A-Z]+?' % PUNCT)
CAPFIRST = re.compile(r"^%s*?([A-Za-z])" % PUNCT)
SMALL_FIRST = re.compile(r'^(%s*)(%s)\b' % (PUNCT, SMALL), re.I)
SMALL_LAST = re.compile(r'\b(%s)%s?$' % (SMALL, PUNCT), re.I)
SUBPHRASE = re.compile(r'([:.;?!][ ])(%s)' % SMALL)

def titlecase(text):

    """
    Titlecases input text

    This filter changes all words to Title Caps, and attempts to be clever
    about *un*capitalizing SMALL words like a/an/the in the input.

    The list of "SMALL words" which are not capped comes from
    the New York Times Manual of Style, plus 'vs' and 'v'.

    """

    words = re.split('\s', text)
    line = []
    for word in words:
        if INLINE_PERIOD.search(word) or UC_ELSEWHERE.match(word):
            line.append(word)
            continue
        if SMALL_WORDS.match(word):
            line.append(word.lower())
            continue
        line.append(CAPFIRST.sub(lambda m: m.group(0).upper(), word))

    line = " ".join(line)

    line = SMALL_FIRST.sub(lambda m: '%s%s' % (
        m.group(1),
        m.group(2).capitalize()
    ), line)

    line = SMALL_LAST.sub(lambda m: m.group(0).capitalize(), line)

    line = SUBPHRASE.sub(lambda m: '%s%s' % (
        m.group(1),
        m.group(2).capitalize()
    ), line)

    return line


if __name__ == '__main__':
    if not sys.stdin.isatty():
        for line in sys.stdin:
            print titlecase(line)


