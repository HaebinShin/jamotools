# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super, filter, map, zip)

import unittest
from ddt import ddt, data, file_data
import jamotools
import six

def _hex_string_to_str(s):
    return six.unichr(int(s,16))

@ddt
class TestJamotools(unittest.TestCase):
    @file_data("data/rule1.json")
    def test_rule1(self, input, output):
        v = jamotools.Vectorizationer(rule=jamotools.rules.RULE_1, \
                                    max_length=None, \
                                    prefix_padding_size=0)
        pred = v.vectorize(input)
        self.assertTrue(pred.tolist()==output)

    def test_is_syllable(self):
        true_ = jamotools.is_syllable('한')
        false_int = jamotools.is_syllable(1)
        false_mix = jamotools.is_syllable('ㄱa')
        self.assertEqual(true_, True)
        self.assertEqual(false_int, False)
        self.assertEqual(false_mix, False)

    @file_data("data/normalize_to_compat_jamo.json")
    def test_normalize_to_compat_jamo(self, input, output):
        input = ''.join([_hex_string_to_str(h) for h in input])
        pred = jamotools.normalize_to_compat_jamo(input)
        output = ''.join([_hex_string_to_str(h) for h in output])
        self.assertEqual(pred, output)

    @file_data("data/split_syllables_char.json")
    def test_split_syllables_char(self, input, output, jamo_type):
        pred = jamotools.split_syllables(input, jamo_type=jamo_type)
        output = ''.join([_hex_string_to_str(h) for h in output])
        self.assertEqual(pred, output)

    @file_data("data/split_syllables.json")
    def test_split_syllables(self, input, output, jamo_type):
        pred = jamotools.split_syllables(input, jamo_type=jamo_type)
        output = ''.join([_hex_string_to_str(h) for h in output])
        self.assertEqual(pred, output)

    @file_data("data/join_jamos_char.json")
    def test_join_jamos_char(self, input, output):
        pred = jamotools.join_jamos_char(_hex_string_to_str(input[0]), \
                                         _hex_string_to_str(input[1]), \
                                         _hex_string_to_str(input[2]))
        self.assertEqual(pred, output)

    @file_data("data/join_jamos.json")
    def test_join_jamos(self, input, output):
        input = ''.join([_hex_string_to_str(h) for h in input])
        pred = jamotools.join_jamos(input)
        self.assertEqual(pred, output)

if __name__ == '__main__':
    unittest.main()