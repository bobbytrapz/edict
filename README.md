An edict parser

You can download edict from http://www.edrdg.org/jmdict/edict.html

## Install

Just save [edict.py](/edict.py?raw=true) to where you need it.

## Usage

```
import edict
EDICT_FILE_PATH = ...
entries = edict.parse_dictionary(EDICT_FILE_PATH)
```

An edict.Entry looks like this:

```
Entry(kanji=[Word(text='大丈夫')], kana=[Word(text='だいじょうぶ', mark=['common']), Word(text='だいじょぶ')], definitions=[Definition(words=[Word(text='safe'), Word(text='all right'), Word(text='alright'), Word(text='OK'), Word(text='okay'), Word(text='sure')], pos=['adjectival nouns or quasi-adjectives (keiyodoshi)']), Definition(words=[Word(text='certainly'), Word(text='surely'), Word(text='undoubtedly')], pos=['adverb (fukushi)']), Definition(words=[Word(text='(だいじょうぶ only)   great man', mark=['archaism']), Word(text='fine figure of a man')], pos=['noun (common) (futsuumeishi)'])])
```

Should be reasonably fast. Parsing edict2 took around 5 seconds on my machine.
