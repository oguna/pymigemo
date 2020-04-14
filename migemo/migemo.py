import argparse
import re
from os import path
from typing import List

from . import characterconverter
from . import migemocompactdictionary
from . import regexgenerator
from . import regexoperator
from . import romajiconverter


class Migemo:
    def __init__(self):
        self.entries = []
        with open(path.dirname(path.abspath(__file__)) + '/dict/migemo-compact-dict', mode='rb') as file:
            self.dictionary = migemocompactdictionary.MigemoCompactDictionary(file)
        self.regex_operator = regexoperator.RegexOperators.DEFAULT.value

    def query(self, query: str) -> str:
        words = Migemo.parse_query(query)
        results = []
        for word in words:
            results.append(self.query_word(word))
        return ''.join(results)

    def query_word(self, query: str) -> str:
        generator = regexgenerator.RegexGenerator(self.regex_operator)
        generator.add(query)
        lower = query.lower()
        for i in self.dictionary.predictive_search(lower):
            generator.add(i)
        zenkaku = characterconverter.han2zen(query)
        generator.add(zenkaku)
        hankaku = characterconverter.zen2han(query)
        generator.add(hankaku)
        for hiragana in romajiconverter.convert_romaji_to_hiragana_predictively(query):
            generator.add(hiragana)
            for i in self.dictionary.predictive_search(hiragana):
                generator.add(i)
        return generator.generate()

    @staticmethod
    def parse_query(q: str) -> List[str]:
        p = re.compile(r'[^A-Z\s]+|[A-Z]{2,}|[A-Z][a-z]+')
        return p.findall(q)


def main():
    parser = argparse.ArgumentParser(description="pymigemo - Py/Migemo Library")
    # parser.add_argument('-d', '--dict', nargs=1, help='use a file <dict> for dictionary.')
    parser.add_argument('-q', '--quiet', action='store_true', help='show no message except results.')
    parser.add_argument('-v', '--vim', action='store_true', help='use vim style regexp.')
    parser.add_argument('-e', '--emacs', action='store_true', help='use vim style regexp.')
    parser.add_argument('-n', '--newline', action='store_true', help='don\'t use newline match.')
    parser.add_argument('-w', '--word', nargs=1, help='expand a <word> and soon exit.')
    args = parser.parse_args()

    migemo = Migemo()

    if args.vim:
        if args.newline:
            migemo.regex_operator = regexoperator.RegexOperators.VIM_NONEWLINE.value
        else:
            migemo.regex_operator = regexoperator.RegexOperators.VIM_NEWLINE.value
    elif args.emacs:
        if args.newline:
            migemo.regex_operator = regexoperator.RegexOperators.EMACS_NONEWLINE.value
        else:
            migemo.regex_operator = regexoperator.RegexOperators.EMACS_NEWLINE.value

    if args.word:
        answer = migemo.query(args.word[0])
        if answer:
            print(answer)
    else:
        while True:
            if args.quiet:
                query = input()
            else:
                query = input('QUERY: ')
            if not query:
                break
            pattern = migemo.query(query)
            if args.quiet:
                print(pattern)
            else:
                print('PATTERN:', pattern)


if __name__ == '__main__':
    main()
