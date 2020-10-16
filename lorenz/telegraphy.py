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
    def encode(message, alphabet=BP_SHIFTLESS_ITA2, complain=True):
        """ Encode a string of English letters as a list of five-bit ITA2
        codepoints.

        Illegal characters normally trigger a RuntimeError. This can be 
        disabled by setting the `complain` parameter to a truthy value.
        """

        message = message.upper()

        stream = []
        for character in message:
            if character in alphabet:
                stream.append(alphabet.index(character))
            elif complain:
                raise RuntimeError(
                  f"Teleprinter could not encrypt character \"{character}\"."
                )
        
        return stream

    @staticmethod
    def decode(stream):
        """ Decode a list of five-bit ITA2 codepoints to a string of English 
        letters.
        """
        
        message = ""
        for character in stream:
            if (character < 0) or (character >= 32):
                raise RuntimeError(
                  "Teleprinter could not decrypt character " +\
                  f"\"{bin(character)[2:].zfill(5)}\"."
                )
            message += BP_SHIFTLESS_ITA2[character]
        
        return message

    @staticmethod
    def dotcross(stream):
        """ Convert a stream of zeroes and ones to the corresponding dots (.) 
        and crosses (+) representation.
        """

        if all(bit in [0, 1] for bit in stream):
            return "".join(".+"[bit] for bit in stream)

        raise RuntimeError("a non-binary sequence was supplied.")

    @staticmethod
    def binarify(stream):
        """ Convert a stream of dots (.) and crosses (+) to the corresponding
        stream of zeroes and ones.
        """

        if all(symbol in [".", "+"] for symbol in stream):
            return [".+".index(symbol) for symbol in stream]

        raise RuntimeError("a non-dotcross sequence was supplied.")
