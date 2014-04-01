from urllib import request
import os
import sys

tag_length = 2
if len(sys.argv) == 2:
    tag_length = int(sys.argv[1])

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

URL = 'https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry'
lines = request.urlopen(URL).read().decode().split('\n')
entry = {'type': '', 'name': '', 'tag': ''}
langs = []
for line in lines[1:]:
    key, separator, value = line.partition(': ')
    if line == '%%':
        if entry['type'] == 'language' and entry['tag'] and entry['name']:
            langs.append((entry['tag'], entry['name']))
        entry = {'type': '', 'name': '', 'tag': ''}
        last = 'None'
    elif key == 'Type':
        entry['type'] = value
        last = 'type'
    elif key == 'Subtag' and len(value) <= tag_length:
        entry['tag'] = value
        last = 'tag'
    elif key == 'Description' and not entry['name']:
        entry['name'] = value
        last = 'name'
    elif key == 'Deprecated' or key == 'Preferred-Value':
        entry = {'type': '', 'name': '', 'tag': ''}
    elif line.startswith('  '):
        entry[last] += line[1:]

if entry['type'] == 'language' and entry['tag'] and entry['name']:
    langs.append((entry['tag'], entry['name']))

file = open(os.path.join(parent_dir, 'langs.py'), 'w')
file.write('''#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import glob
import os

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    # Allows this module to be executed without Django installed.
    _ = lambda x: x\n\n''')

file.write('LANGS = {\n')

for lang in langs:
    file.write('    "{0}", _("{1}"),\n'.format(lang[0], lang[1]))

file.write('}\n')
file.close()
