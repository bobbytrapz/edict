#!/usr/bin/env python3

import unittest
import edict


class TestEdict(unittest.TestCase):
    def test_parse_entry(self):
        raw = '大丈夫 [だいじょうぶ(P);だいじょぶ] /(adj-na) (1) safe/all right/alright/OK/okay/sure/(adv) (2) certainly/surely/undoubtedly/(n) (3) (だいじょうぶ only) (arch) (See 大丈夫・だいじょうふ) great man/fine figure of a man/(P)/EntL1414150X/\n'
        should_be = "Entry(kanji=['大丈夫'], kana=['だいじょうぶ', 'だいじょぶ'], pos=['adjectival nouns or quasi-adjectives (keiyodoshi)', 'adverb (fukushi)', 'noun (common) (futsuumeishi)'], mark=['common', 'archaism', 'common'], region=[], definitions=[['safe', 'all right', 'alright', 'OK', 'okay', 'sure'], ['certainly', 'surely', 'undoubtedly'], ['(だいじょうぶ only)   great man', 'fine figure of a man']])"
        entry = edict.parse_entry(raw)
        self.assertEqual(str(entry), should_be)


if __name__ == '__main__':
    unittest.main()
