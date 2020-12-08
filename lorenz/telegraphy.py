#!/usr/bin/env python
# -*- coding: utf-8 -*-

# telegraphy.py
# Copyright (c) 2020 Hugh Coleman
#
# This file is part of hughcoleman/lorenz, a historically accurate simulator of
# the Lorenz SZ40 Cipher Machine. It is released under the MIT License (see
# LICENSE.)

""" Aids in the conversion English text (expressed in "Bletchley Shiftless"
format) to and from the five-bit ITA2 "Baudot" standard.
"""

# The folks at Bletchley Park used a "shiftless" variant of the ITA2, as it
# allowed for easier cryptanalysis.
BP_SHIFTLESS_ITA2 = list("/T3O9HNM4LRGIPCVEZDBSYFXAWJ+UQK8")


class Teleprinter:
    """ This class implements static methods that convert English text to and
    from the ITA2/"Baudot" standard. """

    @staticmethod
    def encode(message, alphabet=BP_SHIFTLESS_ITA2):
        """ Encode a string of English letters as a list of five-bit ITA2
        codepoints.

        Illegal characters trigger a RuntimeError.
        """

        message = message.upper()

        if any(character not in alphabet for character in message):
            raise RuntimeError("illegal character in message")

        return [alphabet.index(character) for character in message]

    @staticmethod
    def decode(stream):
        """ Decode a list of five-bit ITA2 codepoints to a string of English
        letters.
        """

        if any((character < 0) or (character >= 32) for character in stream):
            raise RuntimeError("illegal byte in stream")

        return "".join(BP_SHIFTLESS_ITA2[character] for character in stream)

    @staticmethod
    def dotcross(stream):
        """ Convert a stream of zeroes and ones to the corresponding dots (.)
        and crosses (+) representation.
        """

        if any(bit not in [0, 1] for bit in stream):
            raise RuntimeError("a non-binary sequence was supplied.")

        return "".join(".+"[bit] for bit in stream)

    @staticmethod
    def binarify(stream):
        """ Convert a stream of dots (.) and crosses (+) to the corresponding
        stream of zeroes and ones.
        """

        if any(symbol not in [".", "+"] for symbol in stream):
            raise RuntimeError("a non-dotcross sequence was supplied.")

        return [".+".index(symbol) for symbol in stream]
