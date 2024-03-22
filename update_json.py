#!/usr/bin/env python3

import os
import posixpath
from urllib.parse import quote
import re
import json


def regexReplace(string, search, replacement):
    return re.compile(search).sub(replacement, string)


def shorten_string(input_string):
    if len(input_string) <= 100:
        return input_string
    else:
        return input_string[:97] + '...'


# determine whether to truncate
DO_TRUNCATE = True

json_data = {}
languageCount = 0
languagesText = ""
content = ""

# List the available languages
for directory in sorted(os.listdir('.')):
    if not (directory == '.' or directory == '..' or directory[0] == '.'
            or os.path.isfile(directory)):
        for filename in sorted(os.listdir(directory), key=lambda s: s.lower()):
            if os.path.isfile(os.path.join(directory, filename)):
                language = (os.path.splitext(filename)[0].replace(
                    "-", "-").replace("∕", "/").replace("＼", "\\").replace(
                    "˸", ":").replace("∗", "*").replace("？", "?").replace(
                    "＂",
                    "\"").replace("﹤",
                                  "<").replace("﹥",
                                               ">").replace("❘", "|"))
                languagesText += f'* [{language}]({posixpath.join(quote(directory), quote(filename))})\n'
                languageCount += 1

                json_data[languageCount] = {}
                json_data[languageCount]['language'] = language
                json_data[languageCount]['path'] = f'{posixpath.join(quote(directory), quote(filename))}'

                with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as file:
                    try:
                        content = file.read()
                    except UnicodeDecodeError:
                        content = file.read().decode('latin-1')
                    json_data[languageCount]['content'] = shorten_string(content) if DO_TRUNCATE else content

file_path = 'data.json'
with open(file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)
