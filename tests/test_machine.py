#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_machine.py
# Copyright (c) 2020 Hugh Coleman
#
# This file is part of hughcoleman/lorenz, a historically accurate simulator of
# the Lorenz SZ40 Cipher Machine. It is released under the MIT License (see
# LICENSE.)
import unittest

from lorenz.machines import SZ40
from lorenz.patterns import KH_CAMS
from lorenz.telegraphy import Teleprinter

ciphertext = Teleprinter.encode("9W3UMKEGPJZQOKXC")
plaintext = Teleprinter.encode("ATTACK99AT99DAWN")


class TestSZ40(unittest.TestCase):
    def test__encrypt(self):
        machine = SZ40(rotors=KH_CAMS)

        self.assertEqual(ciphertext, machine.feed(plaintext))

    def test__decrypt(self):
        machine = SZ40(rotors=KH_CAMS)

        self.assertEqual(plaintext, machine.feed(ciphertext))
