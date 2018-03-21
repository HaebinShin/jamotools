# -*- coding: utf-8 -*-
"""
Based on https://github.com/kaniblu/hangul-utils/blob/master/hangul_utils/jamo.py.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super, filter, map, zip)

import sys
import six
import functools
from .unicode_table import *


def __c(x):
    return six.unichr(x)


def __items(x):
    return six.iteritems(x)


if sys.version_info[0] <= 2:
    import codecs
    def __u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def __u(x):
        return x

JAMO_CHOSEONG = list(map(__c, JAMO_UNICODE['CHOSEONG']))
JAMO_JUNGSEONG = list(map(__c, JAMO_UNICODE['JUNGSEONG']))
JAMO_JONGSEONG = list(map(__c, JAMO_UNICODE['JONGSEONG']))
JAMO_SET = set(JAMO_CHOSEONG+JAMO_JUNGSEONG+JAMO_JONGSEONG)

HALFWIDTH_CHOSEONG = list(map(__c, HALFWIDTH_UNICODE['CHOSEONG']))
HALFWIDTH_JUNGSEONG = list(map(__c, HALFWIDTH_UNICODE['JUNGSEONG']))
HALFWIDTH_JONGSEONG = list(map(__c, HALFWIDTH_UNICODE['JONGSEONG']))
HALFWIDTH_SET = set(HALFWIDTH_CHOSEONG+HALFWIDTH_JUNGSEONG+HALFWIDTH_JONGSEONG)

COMPAT_CHOSEONG = list(map(__c, COMPAT_UNICODE['CHOSEONG']))
COMPAT_JUNGSEONG = list(map(__c, COMPAT_UNICODE['JUNGSEONG']))
COMPAT_JONGSEONG = list(map(__c, COMPAT_UNICODE['JONGSEONG']))
COMPAT_SET = set(COMPAT_CHOSEONG+COMPAT_JUNGSEONG+COMPAT_JONGSEONG)

CHOSEONG = 0x001
JUNGSEONG = 0x010
JONGSEONG = 0x100

COMPAT_TYPE_CHARLIST = {CHOSEONG: COMPAT_CHOSEONG, JUNGSEONG: COMPAT_JUNGSEONG, JONGSEONG: COMPAT_JONGSEONG}
COMPAT_TYPE_CHARSET = dict(map(lambda x: (x[0], set(x[1])), __items(COMPAT_TYPE_CHARLIST)))
COMPAT_TYPE_INDEXDICT = dict(
    map(lambda x: (x[0], dict([(c, i) for i, c in enumerate(x[1])])),
        __items(COMPAT_TYPE_CHARLIST)))

def is_syllable(x):
    if isinstance(x, str) and len(x)==1:
        return 0xAC00 <= ord(x) <= 0xD7A3
    else:
        return False


def __check_cho_jung_jongseong(x):
    t = 0x000
    for type_code, jamo_set in __items(COMPAT_TYPE_CHARSET):
        if x in jamo_set:
            t |= type_code

    return t

def normalize_to_compat_jamo(jamo_sequence):
    """Normalize Jamo to Hangul Compatibility Jamo

    Args:
        jamo_sequence: A unicode jamo_sequence.

    Return: 
        A converted unicode jamo_sequence.
    """
    if jamo_sequence==None:
        return jamo_sequence
        
    x_arr = []
    for x in jamo_sequence:
        if x in JAMO_SET:
            x_arr.append(__c(JAMO_TO_COMPAT_UNICODE_MAP[ord(x)]))
        elif x in HALFWIDTH_SET:
            x_arr.append(__c(HALFWIDTH_TO_COMPAT_UNICODE_MAP[ord(x)]))
        else:
            x_arr.append(x)
    return ''.join(x_arr)


def split_syllable_char(syllable, jamo_type='JAMO'):
    """Splits a given korean character into components.

    Args:
        syllable: A complete korean syllable.
        jamo_type: A type of jamo unicode representation (optional).
            Valid values for jamo_type are 'JAMO', 'COMPAT', 'HALFWIDTH'.

            'JAMO' is in the range of 0x1100 ~ 0x11FF that the range is divided into 
            chosung, jungseong, jongseong.
            (http://unicode.org/charts/PDF/U1100.pdf)

            'COMPAT' is Hangul Compatibility Jamo range of 0x3130 ~ 0x318F.
            (http://unicode.org/charts/PDF/U3130.pdf)

            'HALFWIDTH' is Halfwidth Hangul variants range of 0xFFA1 ~ 0xFFDC.
            (http://unicode.org/charts/PDF/UFF00.pdf)

    Return: 
        A tuple of basic jamos that constitutes the given syllable.
    """
    if len(syllable) != 1:
        raise ValueError("Input string must have exactly one syllable.")

    if not is_syllable(syllable):
        raise ValueError(
            "Input string does not contain a valid Korean syllable.")

    if jamo_type not in ['JAMO', 'COMPAT', 'HALFWIDTH']:
        raise ValueError(
            "jamo_type expected in ['JAMO', 'COMPAT', 'HALFWIDTH'], but got {}".format(jamo_type))

    diff = ord(syllable) - 0xAC00
    _m = diff % 28
    _d = (diff - _m) // 28

    choseong_index = _d // 21
    jungseong_index = _d % 21
    jongseong_index = _m

    if jamo_type=='JAMO':
        result_choseong = JAMO_CHOSEONG[choseong_index]
        result_jungseong = JAMO_JUNGSEONG[jungseong_index]
        result_jongseong = JAMO_JONGSEONG[jongseong_index - 1]
    elif jamo_type=='COMPAT':
        result_choseong = COMPAT_CHOSEONG[choseong_index]
        result_jungseong = COMPAT_JUNGSEONG[jungseong_index]
        result_jongseong = COMPAT_JONGSEONG[jongseong_index - 1]
    else:
        result_choseong = HALFWIDTH_CHOSEONG[choseong_index]
        result_jungseong = HALFWIDTH_JUNGSEONG[jungseong_index]
        result_jongseong = HALFWIDTH_JONGSEONG[jongseong_index - 1]

    if not jongseong_index:
        result = (result_choseong, result_jungseong)
    else:
        result = (result_choseong, result_jungseong, result_jongseong)

    return result


def join_jamos_char(choseong, jungseong, jongseong=None):
    """Combines jamos to produce a single syllable.

    Args:
        choseong: choseong jamo.
        jungseong: jungseong jamo.
        jongseong: jongseong jamo (optional).

    Return: 
        A syllable.
    """
    choseong = normalize_to_compat_jamo(choseong)
    jungseong = normalize_to_compat_jamo(jungseong)
    jongseong = normalize_to_compat_jamo(jongseong)
    if choseong not in COMPAT_TYPE_CHARSET[CHOSEONG] or jungseong not in COMPAT_TYPE_CHARSET[
        JUNGSEONG] or (jongseong and jongseong not in COMPAT_TYPE_CHARSET[JONGSEONG]):
        raise ValueError("Given Jamo characters are not valid.")

    choseong_ind = COMPAT_TYPE_INDEXDICT[CHOSEONG][choseong]
    jungseong_ind = COMPAT_TYPE_INDEXDICT[JUNGSEONG][jungseong]
    jongseong_ind = COMPAT_TYPE_INDEXDICT[JONGSEONG][jongseong] + 1 if jongseong else 0

    b = 0xAC00 + 28 * 21 * choseong_ind + 28 * jungseong_ind + jongseong_ind

    result = __c(b)

    assert is_syllable(result)

    return result


def split_syllables(text, jamo_type="COMPAT"):
    """Splits a sequence of Korean syllables to produce a sequence of jamos.

    Irrelevant characters will be ignored.

    Args:
        text: A unicode text string.
        jamo_type: A type of jamo unicode representation (optional).
            Valid values for jamo_type are 'JAMO', 'COMPAT', 'HALFWIDTH'.

            'JAMO' is in the range of 0x1100 ~ 0x11FF that the range is divided into 
            chosung, jungseong, jongseong.
            (http://unicode.org/charts/PDF/U1100.pdf)

            'COMPAT' is Hangul Compatibility Jamo range of 0x3130 ~ 0x318F.
            (http://unicode.org/charts/PDF/U3130.pdf)

            'HALFWIDTH' is Halfwidth Hangul variants range of 0xFFA1 ~ 0xFFDC.
            (http://unicode.org/charts/PDF/UFF00.pdf)

    Returns: 
        A converted unicode jamo string.
    """
    new_string = ""
    for s in text:
        if not is_syllable(s):
            new_s = s
        else:
            new_s = "".join(split_syllable_char(s, jamo_type))
        new_string += new_s

    return new_string


def join_jamos(jamos):
    """Combines a sequence of jamos to produce a sequence of syllables.

    Irrelevant characters will be ignored.

    Args:
        jamos: A unicode jamo string.

    Return: 
        A converted unicode text string.
    """
    last_t = 0
    queue = []
    new_string = ""

    def flush(queue, n=0):
        new_queue = []

        while len(queue) > n:
            new_queue.append(queue.pop())

        if len(new_queue) == 1:
            result = new_queue[0]
        elif len(new_queue) >= 2:
            try:
                result = join_jamos_char(*new_queue)
            except ValueError:
                # Invalid jamo combination
                result = "".join(new_queue)
        else:
            result = None

        return result

    jamos = normalize_to_compat_jamo(jamos)
    for c in jamos:
        if c not in COMPAT_SET:
            if queue:
                new_c = flush(queue) + c
            else:
                new_c = c

            last_t = 0
        else:
            t = __check_cho_jung_jongseong(c)
            new_c = None

            if t & JONGSEONG == JONGSEONG:
                if not (last_t == JUNGSEONG):
                    new_c = flush(queue)
            elif t == CHOSEONG:
                new_c = flush(queue)
            elif t == JUNGSEONG:
                if last_t & CHOSEONG == CHOSEONG:
                    new_c = flush(queue, 1)
                else:
                    new_c = flush(queue)

            last_t = t
            queue.insert(0, c)

        if new_c:
            new_string += new_c

    if queue:
        new_string += flush(queue)

    return new_string
