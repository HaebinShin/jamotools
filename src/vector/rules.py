# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super, filter, map, zip)

from ..jamo.hangul_utils import split_syllables
from ..jamo.unicode_table import JAMO_UNICODE
import numpy as np

class RuleBase(object):
    @property
    def symbols(self):
        raise NotImplementedError

    @property
    def maps(self):
        raise NotImplementedError

    @property
    def pad_index(self):
        raise NotImplementedError

    def convert(self):
        raise NotImplementedError

class InvalidRuleError(Exception):
    """Raise when invalid rule.
    """
    pass

PAD = '<PAD>'
UNK = '<UNK>'



RULE_MIN = -1
RULE_1 = 0
RULE_MAX = 1

def get_rule(val):
    """Factory function to get a RULE class.

    Args:
        val: Constant which means each rule.

    Return: 
        RULE instance.
    """
    def _rule_cls_factory(val):
        if val==RULE_1:
            return Rule1()

    if RULE_MIN < val < RULE_MAX:
        return _rule_cls_factory(val)
    else:
        raise InvalidRuleError("{} is not a valid rule".format(val))


class Rule1(RuleBase):
    """Vectorize Rule1.

    Vectorize when each character belongs to Jamo, alphabet, number, special character, <PAD>,
    otherwise convert to <UNK>.
    """
    def __init__(self):
        super().__init__()
        
        self._symbols = []
        self._symbols.append(PAD)
        self._symbols.append(UNK)
        for modern_chosung in JAMO_UNICODE['CHOSEONG']:
            self._symbols.append(chr(modern_chosung))
        for modern_jungsung in JAMO_UNICODE['JUNGSEONG']:
            self._symbols.append(chr(modern_jungsung))
        for modern_jongsung in JAMO_UNICODE['JONGSEONG']:
            self._symbols.append(chr(modern_jongsung))
        for alphabet in range(ord('a'), ord('z')+1):
            self._symbols.append(chr(alphabet))
        for number in range(0, 9+1):
            self._symbols.append(str(number))
        for special in ' .,/()"*:-%':
            self._symbols.append(special)

        self._vectorize_symbol_map = dict([(_symbol, np.uint8(i)) for i, _symbol in enumerate(self._symbols)])

    @property
    def symbols(self):
        return self._symbols

    @property
    def symbol_map(self):
        return self._vectorize_symbol_map

    @property
    def pad_index(self):
        return self._vectorize_symbol_map[PAD]

    def convert(self, text):
        """Split syllables string to jamo and vectorize.

        Args:
            text: A unicode string.

        Return: 
            A converted index numpy array.
        """
        jamo_sequence = split_syllables(text, jamo_type='JAMO')
        vec_sequence = []
        for jamo_char in jamo_sequence:
            if jamo_char in self.symbols:
                vec_sequence.append(self._vectorize_symbol_map[jamo_char])
            else:
                vec_sequence.append(self._vectorize_symbol_map[UNK])
        return np.array(vec_sequence, dtype=np.uint8)
