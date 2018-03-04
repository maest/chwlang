from pathlib import Path
import re
from reader.models import Article, Category, DictionaryEntry

def read_cedict(path_to_cedict):
    with open(path_to_cedict, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            trad, simp = line.split(' ')[:2]
            pinyin = line[line.find('[')+1:line.find(']')]
            eng = line[line.find('/') + 1:line.rfind('/')]
            eng = eng.split('/')
            word = {'simplified': simp,
                    'traditional': trad, 
                    'english': eng, 
                    'pinyin': pinyin}
            yield word

def run():
    cedict_path= 'cedict/cedict_ts.u8'
    cedict = list(read_cedict(cedict_path))
    for w in cedict:
        w['pinyin'] = decode_pinyin(w['pinyin'])

    regex = re.compile(r'\[(.+?[0-9])\]')
    for w in cedict:
        new_w = []
        for e in w['english']:
            new_e = regex.sub(lambda m:'['+decode_pinyin(m.group(0))+']', e)
            new_w.append(new_e)
        w['english'] = new_w
    for w in cedict:
        DictionaryEntry(word=w['simplified'],
                        pinyin=w['pinyin'],
                        translation='\n'.join(w['english'])) \
                        .save()

PinyinToneMark = {
    0: "aoeiuv\u00fc",
    1: "\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6",
    2: "\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8",
    3: "\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da",
    4: "\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc",
}

def decode_pinyin(text):
    text = [decode_single_pinyin(p) for p in text.split()]
    return " ".join(text)

def decode_single_pinyin(s):
    s = s.lower()
    r = ""
    t = ""
    for c in s:
        if c >= 'a' and c <= 'z':
            t += c
        elif c == ':':
            assert t[-1] == 'u'
            t = t[:-1] + "\u00fc"
        else:
            if c >= '0' and c <= '5':
                tone = int(c) % 5
                if tone != 0:
                    m = re.search("[aoeiuv\u00fc]+", t)
                    if m is None:
                        t += c
                    elif len(m.group(0)) == 1:
                        t = t[:m.start(0)] + PinyinToneMark[tone][PinyinToneMark[0].index(m.group(0))] + t[m.end(0):]
                    else:
                        if 'a' in t:
                            t = t.replace("a", PinyinToneMark[tone][0])
                        elif 'o' in t:
                            t = t.replace("o", PinyinToneMark[tone][1])
                        elif 'e' in t:
                            t = t.replace("e", PinyinToneMark[tone][2])
                        elif t.endswith("ui"):
                            t = t.replace("i", PinyinToneMark[tone][3])
                        elif t.endswith("iu"):
                            t = t.replace("u", PinyinToneMark[tone][4])
                        else:
                            t += "!"
            r += t
            t = ""
    r += t
    return r
