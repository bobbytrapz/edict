#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    edict parser
"""

import re
from dataclasses import dataclass, field
from typing import List

POS_LOOKUP = {
    'adj': 'former adjective classification (being removed)',
    'adj-f': 'noun or verb acting prenominally (other than the above)',
    'adj-i': 'adjective (keiyoushi)',
    'adj-na': 'adjectival nouns or quasi-adjectives (keiyodoshi)',
    'adj-no': "nouns which may take the genitive case particle `no'",
    'adj-pn': 'pre-noun adjectival (rentaishi)',
    'adj-t': "`taru' adjective",
    'adv': 'adverb (fukushi)',
    'adv-n': 'adverbial noun',
    'adv-to': "adverb taking the `to' particle",
    'aux': 'auxiliary',
    'aux-adj': 'auxiliary adjective',
    'aux-v': 'auxiliary verb',
    'conj': 'conjunction',
    'ctr': 'counter',
    'exp': 'Expressions (phrases, clauses, etc.)',
    'int': 'interjection (kandoushi)',
    'iv': 'irregular verb',
    'n': 'noun (common) (futsuumeishi)',
    'n-adv': 'adverbial noun (fukushitekimeishi)',
    'n-pref': 'noun, used as a prefix',
    'n-suf': 'noun, used as a suffix',
    'n-t': 'noun (temporal) (jisoumeishi)',
    'num': 'numeric',
    'pn': 'pronoun',
    'pref': 'prefix',
    'prt': 'particle',
    'suf': 'suffix',
    'v1': 'Ichidan verb',
    'v2a-s': "Nidan verb with 'u' ending (archaic)",
    'v4h': "Yodan verb with `hu/fu' ending (archaic)",
    'v4r': "Yodan verb with `ru' ending (archaic)",
    'v5': 'Godan verb (not completely classified)',
    'v5aru': 'Godan verb - -aru special class',
    'v5b': "Godan verb with `bu' ending",
    'v5g': "Godan verb with `gu' ending",
    'v5k': "Godan verb with `ku' ending",
    'v5k-s': 'Godan verb - iku/yuku special class',
    'v5m': "Godan verb with `mu' ending",
    'v5n': "Godan verb with `nu' ending",
    'v5r': "Godan verb with `ru' ending",
    'v5r-i': "Godan verb with `ru' ending (irregular verb)",
    'v5s': "Godan verb with `su' ending",
    'v5t': "Godan verb with `tsu' ending",
    'v5u': "Godan verb with `u' ending",
    'v5u-s': "Godan verb with `u' ending (special class)",
    'v5uru': 'Godan verb - uru old class verb (old form of Eru)',
    'v5z': "Godan verb with `zu' ending",
    'vi': 'intransitive verb',
    'vk': 'kuru verb - special class',
    'vn': 'irregular nu verb',
    'vs': 'noun or participle which takes the aux. verb suru',
    'vs-c': 'su verb - precursor to the modern suru',
    'vs-i': 'suru verb - irregular',
    'vs-s': 'suru verb - special class',
    'vt': 'transitive verb',
    'vz': 'Ichidan verb - zuru verb - (alternative form of -jiru verbs)'
}

MARKING_LOOKUP = {
    'X': 'rude or X-rated term',
    'abbr': 'abbreviation',
    'arch': 'archaism',
    'ateji': 'ateji (phonetic) reading',
    'chn': "children's language",
    'col': 'colloquialism',
    'derog': 'derogatory term',
    'eK': 'exclusively kanji',
    'ek': 'exclusively kana',
    'fam': 'familiar language',
    'fem': 'female term or language',
    'gikun': 'gikun (meaning) reading',
    'hon': 'honorific or respectful (sonkeigo) language',
    'hum': 'humble (kenjougo) language',
    'iK': 'word containing irregular kanji usage',
    'id': 'idiomatic expression',
    'ik': 'word containing irregular kana usage',
    'io': 'irregular okurigana usage',
    'm-sl': 'manga slang',
    'male': 'male term or language',
    'male-sl': 'male slang',
    'oK': 'word containing out-dated kanji',
    'obs': 'obsolete term',
    'obsc': 'obscure term',
    'ok': 'out-dated or obsolete kana usage',
    'on-mim': 'onomatopoeic or mimetic word',
    'poet': 'poetical term',
    'pol': 'polite (teineigo) language',
    'rare': 'rare (now replaced by "obsc")',
    'sens': 'sensitive word',
    'sl': 'slang',
    'uK': 'word usually written using kanji alone',
    'uk': 'word usually written using kana alone',
    'vulg': 'vulgar expression or word',
    'P': 'common'
}

REGION_LOOKUP = {
    'kyb': 'Kyoto-ben',
    'osb': 'Osaka-ben',
    'ksb': 'Kansai-ben',
    'ktb': 'Kantou-ben',
    'tsb': 'Tosa-ben',
    'thb': 'Touhoku-ben',
    'tsug': 'Tsugaru-ben',
    'kyu': 'Kyuushuu-ben',
    'rkb': 'Ryuukyuu-ben',
}

FIELD_LOOKUP = {
    'Buddh': 'Buddhist term',
    'MA': 'martial arts term',
    'comp': 'computer terminology',
    'food': 'food term',
    'geom': 'geometry term',
    'gram': 'grammatical term',
    'ling': 'linguistics terminology',
    'math': 'mathematics',
    'mil': 'military',
    'physics': 'physics terminology'
}

MARKING_LOOKUP.update(REGION_LOOKUP)
MARKING_LOOKUP.update(FIELD_LOOKUP)


@dataclass
class Word:
    text: str = ''
    mark: List[str] = field(default_factory=list)
    region: List[str] = field(default_factory=list)

    def __repr__(self):
        s = f'Word(text={self.text!r}'
        if self.mark:
            s += f', mark={self.mark!r}'
        if self.region:
            s += f', region={self.region!r}'
        s += ')'
        return s


@dataclass
class Definition:
    words: List[Word] = field(default_factory=list)
    pos: List[str] = field(default_factory=list)


@dataclass
class Entry:
    raw: str = field(repr=False)
    kanji: List[Word] = field(default_factory=list)
    kana: List[Word] = field(default_factory=list)
    definitions: List[Definition] = field(default_factory=list)
    ent: List[str] = field(repr=False, default_factory=list)
    ref: List[str] = field(repr=False, default_factory=list)

    @property
    def words(self):
        return [w.text for w in self.kanji + self.kana]


def parse_entry(raw: str) -> Entry:
    ''' parse an edict dictionary entry '''
    tokre = re.compile(
        r"([^\[\]\/;]+)|;|.?\[|\].?|\/").match
    info_re = re.compile(r'\(([\w\d\-\s:,]+)\)').findall
    mark_re = re.compile(r'\(([\w\d\-\s:,]+)\)').findall
    see_re = re.compile(r"\(See [^\)]+\)").findall
    defnum_re = re.compile(r"\((\d+)\)").findall

    entry = Entry(raw)

    # add to the latest entry definition
    def _add_definition(words, pos, mark, region):
        entry.definitions[-1].pos.extend(pos)
        entry.definitions[-1].words.extend(Word(w, mark, region)
                                           for w in words)

    def _japanese(subitem):
        mark = list()
        markings = mark_re(subitem)
        for marking in markings:
            m = MARKING_LOOKUP.get(marking)
            if m:
                subitem = subitem.replace(f'({marking})', '')
                mark.append(m)
        return subitem.strip(), mark

    def _kanji(subitem):
        subitem, mark = _japanese(subitem)
        word = Word(subitem, mark=mark)
        entry.kanji.append(word)

    def _kana(subitem):
        subitem, mark = _japanese(subitem)
        word = Word(subitem, mark=mark)
        entry.kana.append(word)

    def _gloss(subitem):
        region = list()
        pos = list()
        mark = list()

        # check if entry listing
        if subitem.startswith('Ent'):
            entry.ent.append(subitem)
            return
        # check for references
        references = see_re(subitem)
        for ref in references:
            subitem = subitem.replace(ref, '').strip()
            ref = ref.replace('See ', '').replace('(', '').replace(')', '')
            ref = ref.strip()
            entry.ref.extend(r for r in ref.split(',') if r)
        # check if marking
        markings = mark_re(subitem)
        for marking in markings:
            if marking.endswith(':'):
                mark = marking[:-1]
                r = REGION_LOOKUP.get(mark)
                if r:
                    subitem = subitem.replace(f'({marking})', '')
                    region.append(r)
            else:
                m = MARKING_LOOKUP.get(marking)
                if m:
                    subitem = subitem.replace(f'({marking})', '')
                    mark.append(m)
        # check for additional info in gloss and replace it before adding
        additional_info = info_re(subitem)
        for info in additional_info:
            for info_part in info.split(','):
                p = POS_LOOKUP.get(info_part)
                if p:
                    subitem = subitem.replace(f'({info})', '')
                    pos.append(p)
        # may have been modified and so could be an empty string
        if subitem:
            # add definition
            if not entry.definitions:
                entry.definitions.append(Definition())
            m = defnum_re(subitem)
            if m:
                defnum = int(m[0])
                if defnum > 1:
                    entry.definitions.append(Definition())
                subitem = subitem.replace(f'({defnum})', '')
            words = [g for g in subitem.strip().split(';') if g]
            _add_definition(words, pos, mark, region)

    if '[' in raw:
        mode = _kanji
    else:
        mode = _kana

    ndx = 0
    while ndx < len(raw):
        match = tokre(raw, ndx)
        if not match:
            # we assume this is not an entry
            break
        ndx = match.end()
        token = match.group()
        if token == ' [' or token == '[':
            # begin kana mode
            mode = _kana
        elif token == '] ' or token == ']':
            # begin gloss mode
            mode = _gloss
        elif token == ';':
            # next kana or kanji
            pass
        elif token == '/':
            for gloss in raw[ndx:].split('/'):
                _gloss(gloss)
            break
        else:
            mode(token)

    return entry


def parse_dictionary(edict_path, encoding='EUC-JP') -> List[Entry]:
    with open(str(edict_path), encoding=encoding) as d:
        lines = d.readlines()
    return [parse_entry(raw)
            for raw in lines
            if not raw.startswith('#')]
