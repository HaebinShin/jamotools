# Jamotools

[![Build Status](https://travis-ci.org/HaebinShin/jamotools.svg?branch=master)](https://travis-ci.org/HaebinShin/jamotools)
[![GitHub Tag](https://img.shields.io/github/tag/HaebinShin/jamotools.svg?label=github+tag)](https://github.com/HaebinShin/jamotools/tags)
[![PyPI version](https://img.shields.io/pypi/v/jamotools.svg)](https://pypi.python.org/pypi/jamotools/)
[![Python version](https://img.shields.io/pypi/pyversions/jamotools.svg)](https://pypi.python.org/pypi/jamotools/)
[![License](https://img.shields.io/pypi/l/jamotools.svg)](https://github.com/HaebinShin/jamotools/blob/master/LICENSE)


A library for Korean Jamo split and vectorize.

## Install
```sh
pip install jamotools
```

## Unicode of Korean

According to the Version 9.0.0 database of the Unicode Consortium, the blocks specified in *Hangul* (Korean) in Unicode are as follows.

- Hangul Jamo: 1100 ~ 11FF
- WON SIGN in Currency Symbols: 20A9
- HANGUL DOT TONE MARK in CJK Symbols and Punctuation: 302E ~ 302F
- Hangul Compatibility Jamo : 3130 ~ 318F
- Hangul in Enclosed CJK Letters and Months: 3200 ~ 321E, 3260 ~ 327F
- Hangul Jamo Extended-A : A960 ~ A97F
- Hangul Syllables : AC00 ~ D7AF
- Hangul Jamo Extended-B : D7B0 ~ D7FF
- Halfwidth Hangul variants in Halfwidth and Fullwidth Forms: FFA0 ~ FFDC
- FULLWIDTH WON SIGN in Halfwidth and Fullwidth Forms: FFE6

### Jamo
Hangul is made of basic letters called *Jamo*. In unicode, Jamo is defined by several kinds which contain old Hangul that does not use in nowadays. Jamotools only supports modern Hangul Jamo area as follows.

- [Hangul Jamo][jamo_unicode]: Consist of Choseong, Jungseong, Jongseong. It is divided mordern Hangul and old Hangul that does not use in nowadays. Jamotools supports modern Hangul Jamo area.
    - 1100 ~ 1112 (Choseong)
    - 1161 ~ 1175 (Jungseong)
    - 11A8 ~ 11C2 (Jongseong)
- [Hangul Compatibility Jamo][compat_unicode]: It is a Korean Hangul language area that is compatible with the Hangul character standard (KS X 1001). It is not divided Choseong, Jungseong, Jongseong.
    - 3131 ~ 3163 (modern Hangul Jamo area)
- [Halfwidth Hangul variants][halfwidth_unicode]: This is the Korean half-width symbol area. Only modern Korean Jamo exists. The general Korean Hangul characterization method is the full-width.
    - FFA1 ~ FFDC


## Manipulating Korean Jamo
API for split syllables and join jamos to syllable is based on [hangul-utils][hangul_utils_apis]. 

 - `split_syllables`: Converts a string of syllables to a string of jamos, can be select which convert unicode type.
 - `join_jamos`: Converts a string of jamos to a string of syllables.
 - `normalize_to_compat_jamo`: Normalize a string of jamos to a string of *Hangul Compatibility Jamo*.

```py
>>> import jamotools
>>> print(jamotools.split_syllable_char(u"안"))
('ㅇ', 'ㅏ', 'ㄴ')

>>> print(jamotools.split_syllables(u"안녕하세요"))
ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ

>>> sentence = u"앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽.우리 집
    깨죽은 검은 깨 깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 죽먹기를 싫어하더라."
>>> s = jamotools.split_syllables(sentence)
>>> print(s)
ㅇㅏㅍ ㅈㅣㅂ ㅍㅏㅌㅈㅜㄱㅇㅡㄴ ㅂㅜㄺㅇㅡㄴ ㅍㅏㅌ ㅍㅜㅅㅍㅏㅌㅈㅜㄱㅇㅣㄱㅗ,
ㄷㅟㅅㅈㅣㅂ ㅋㅗㅇㅈㅜㄱㅇㅡㄴ ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ ㅋㅗㅇㅈㅜㄱ.ㅇㅜㄹㅣ
ㅈㅣㅂ ㄲㅐㅈㅜㄱㅇㅡㄴ ㄱㅓㅁㅇㅡㄴ ㄲㅐ ㄲㅐㅈㅜㄱㅇㅣㄴㄷㅔ ㅅㅏㄹㅏㅁㄷㅡㄹㅇㅡㄴ
ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ ㅋㅗㅇㅈㅜㄱ ㄲㅐㅈㅜㄱ ㅈㅜㄱㅁㅓㄱㄱㅣㄹㅡㄹ
ㅅㅣㅀㅇㅓㅎㅏㄷㅓㄹㅏ.

>>> sentence2 = jamotools.join_jamos(s)
>>> print(sentence2)
앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽.우리 집 깨죽은 검은 깨
깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 죽먹기를 싫어하더라.

>>> print(sentence == sentence2)
True
```

Jamotools' API supports multiple unicode area of Hangul Jamo for manipulating. Also consists of additional API for manipulating Korean jamo.

```py
>>> sentence = u"자모"

>>> jamos1 = jamotools.split_syllables(sentence, jamo_type="JAMO")
>>> print([hex(ord(c)) for c in jamos1])
['0x110C', '0x1161', '0x1106', '0x1169']
>>> sentence1 = jamotools.join_jamos(jamos1)
>>> print(sentence1)
안녕하세요. hello 1

>>> jamos2 = jamotools.split_syllables(sentence, jamo_type="COMPAT")
>>> print([hex(ord(c)) for c in jamos2])
['0x3148', '0x314F', '0x3141', '0x3157']
>>> sentence2 = jamotools.join_jamos(jamos2)
>>> print(sentence2)
안녕하세요. hello 1

>>> jamos3 = jamotools.split_syllables(sentence, jamo_type="HALFWIDTH")
>>> print([hex(ord(c)) for c in jamos3])
['0xFFB8', '0xFFC2', '0xFFB1', '0xFFCC']
>>> sentence3 = jamotools.join_jamos(jamos3)
>>> print(sentence3)
안녕하세요. hello 1

>>> print(sentence == sentence1 == sentence2 == sentence3)
True

>>> normalize1 = jamotools.normalize_to_compat_jamo(jamos1)
>>> normalize2 = jamotools.normalize_to_compat_jamo(jamos2)
>>> normalize3 = jamotools.normalize_to_compat_jamo(jamos3)
>>> print(jamos1 == jamos2 == jamos3)
False
>>> print(normalize1 == normalize2 == normalize3)
True
```

## Vectorize Korean Jamo
Jamotools support vectorize function following RULE. Each RULE is defined how split sentence to Jamo and convert which type of symbols. It can be used character-level Korean text processing.

- `Vectorizationer`: Class for vectorize text by Rule and pad.

```py
>>> v = jamotools.Vectorizationer(rule=jamotools.rules.RULE_1, \
                                  max_length=None, \
                                  prefix_padding_size=0)
>>> print(v.vectorize(u"안녕"))
[13, 21, 45,  4, 27, 62]
```

### Custom RULE
Jamotools can add user's custom RULE class as following steps.

1. Make custom RULE class which inherit RuleBase (e.g. Rule2) in [rules.py][rules_py] like Rule1.
2. Add constant for custom RULE like [RULE_1][rule_constant].
3. Modify [get_rule][get_rule_function] function to return custom RULE class.

Then it can be use as same as RULE_1 usage.
```py
>>> v = jamotools.Vectorizationer(rule=jamotools.rules.RULE_2, \
                                  max_length=None, \
                                  prefix_padding_size=0)
```

[jamo_unicode]: http://unicode.org/charts/PDF/U1100.pdf
[compat_unicode]: http://unicode.org/charts/PDF/U3130.pdf
[halfwidth_unicode]: http://unicode.org/charts/PDF/UFF00.pdf
[hangul_utils_apis]: https://github.com/kaniblu/hangul-utils/blob/master/README.md#manipulating-korean-characters
[rules_py]: https://github.com/HaebinShin/jamotools/blob/master/jamotools/vector/rules.py
[rule_constant]: https://github.com/HaebinShin/jamotools/blob/master/jamotools/vector/rules.py#L39-L41
[get_rule_function]: https://github.com/HaebinShin/jamotools/blob/master/jamotools/vector/rules.py#L53-L54