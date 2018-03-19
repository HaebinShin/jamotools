# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super, filter, map, zip)

import numpy as np
from . import rules

class Vectorizationer(object):
    def __init__(self, rule, max_length, prefix_padding_size=0):
        self._rule = rules.get_rule(rule)
        self._symbols = self._rule.symbols
        self._symbol_map = self._rule.symbol_map
        self._pad_index = self._rule.pad_index
        self._max_length = max_length
        self._prefix_padding_size = prefix_padding_size
        
    @property
    def max_length(self):
        """Max length after vectorize.
        """
        return self._max_length

    @property
    def symbols(self):
        """Return vectorize symbols.
        """
        return self._symbols

    @property
    def symbol_map(self):
        """Return dictionary (key: symbol, value: index).
        """
        return self._symbol_map

    @property
    def pad_index(self):
        """Return index of <PAD>.
        """
        return self._pad_index

    def vectorize(self, text):
        """Vectorize text by Rule and pad.

        Args:
            text: A unicode string.

        Return: 
            A converted index numpy array with padding.
        """
        vec_sequence = np.array(self._rule.convert(text))
        if self._max_length==None:
            return np.pad(vec_sequence, 
                    pad_width=(self._prefix_padding_size, 0), 
                    mode='constant', 
                    constant_values=(self._rule.pad_index,))
        else:
            postfix_padding_size = self._max_length-min([self._max_length, len(vec_sequence)+self._prefix_padding_size])
            return np.pad(vec_sequence, 
                    pad_width=(self._prefix_padding_size, postfix_padding_size), 
                    mode='constant', 
                    constant_values=(self._rule.pad_index,))[:self._max_length]
