An edict parser

You can download edict from http://www.edrdg.org/jmdict/edict.html

## Install

Just save [edict](/edict.py?raw=true) to where you need it.

## Usage

```
import edict
EDICT_FILE_PATH = ...
entries = edict.parse_dictionary(EDICT_FILE_PATH)
```

An edict.Entry looks like this:

```
Entry(kanji=['大丈夫'], kana=['だいじょうぶ', 'だいじょぶ'], pos=['adjectival nouns or quasi-adjectives (keiyodoshi)', 'adverb (fukushi)', 'noun (common) (futsuumeishi)'], mark=['common', 'archaism', 'common'], region=[])
```

The part of speech for Entry.definitions[0] should be Entry.pos[0]

Should be reasonably fast. Parsing edict2 took about 5 seconds on my machine.
