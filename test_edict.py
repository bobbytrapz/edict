#!/usr/bin/env python3

import unittest
import edict


class TestEdict(unittest.TestCase):
    def test_parse_entry(self):
        raw = '大丈夫 [だいじょうぶ(P);だいじょぶ] /(adj-na) (1) safe/all right/alright/OK/okay/sure/(adv) (2) certainly/surely/undoubtedly/(n) (3) (だいじょうぶ only) (arch) (See 大丈夫・だいじょうふ) great man/fine figure of a man/(P)/EntL1414150X/\n'
        should_be = "Entry(kanji=[Word(text='大丈夫')], kana=[Word(text='だいじょうぶ', mark=['common']), Word(text='だいじょぶ')], definitions=[Definition(words=[Word(text='safe'), Word(text='all right'), Word(text='alright'), Word(text='OK'), Word(text='okay'), Word(text='sure')], pos=['adjectival nouns or quasi-adjectives (keiyodoshi)']), Definition(words=[Word(text='certainly'), Word(text='surely'), Word(text='undoubtedly')], pos=['adverb (fukushi)']), Definition(words=[Word(text='(だいじょうぶ only)   great man', mark=['archaism']), Word(text='fine figure of a man')], pos=['noun (common) (futsuumeishi)'])])"
        entry = edict.parse_entry(raw)
        self.assertEqual(str(entry), should_be)

    def test_parse_edict(self):
        entries = edict.parse_dictionary('edict2')
        self.assertEqual(len(entries), 177086)


if __name__ == '__main__':
    unittest.main()
