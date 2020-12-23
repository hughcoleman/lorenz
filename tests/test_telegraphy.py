#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_telegraphy.py
# Copyright (c) 2020 Hugh Coleman
#
# This file is part of hughcoleman/lorenz, a historically accurate simulator of
# the Lorenz SZ40 Cipher Machine. It is released under the MIT License (see
# LICENSE.)
import unittest

from lorenz.telegraphy import Teleprinter


class TestTeleprinter(unittest.TestCase):
    def test__encode(self):
        self.assertEqual(
            [24, 9, 24, 6, 4, 4, 1, 28, 10, 12, 6, 11],
            Teleprinter.encode("ALAN99TURING"),
        )

        self.assertEqual(
            [19, 12, 9, 9, 4, 4, 1, 28, 1, 1, 16],
            Teleprinter.encode("BILL99TUTTE"),
        )

        self.assertEqual(
            [19, 9, 16, 1, 14, 5, 9, 16, 21, 4, 4, 13, 24, 10, 30],
            Teleprinter.encode("BLETCHLEY99PARK"),
        )

        self.assertEqual(
            [20, 1, 24, 1, 12, 3, 6, 4, 4, 23],
            Teleprinter.encode("STATION99X"),
        )

        # we should also test to ensure that the program complains
        self.assertRaises(
            RuntimeError, Teleprinter.encode, "ILLEGAL CHARACTERS!"
        )

    def test__decode(self):
        self.assertEqual(
            "ALAN99TURING",
            Teleprinter.decode([24, 9, 24, 6, 4, 4, 1, 28, 10, 12, 6, 11]),
        )

        self.assertEqual(
            "BILL99TUTTE",
            Teleprinter.decode([19, 12, 9, 9, 4, 4, 1, 28, 1, 1, 16]),
        )

        self.assertEqual(
            "BLETCHLEY99PARK",
            Teleprinter.decode(
                [19, 9, 16, 1, 14, 5, 9, 16, 21, 4, 4, 13, 24, 10, 30]
            ),
        )

        self.assertEqual(
            "STATION99X",
            Teleprinter.decode([20, 1, 24, 1, 12, 3, 6, 4, 4, 23]),
        )

        self.assertEqual(
            "ILLEGALCHARACTERS",
            Teleprinter.decode(
                [12, 9, 9, 16, 11, 24, 9, 14, 5, 24, 10, 24, 14, 1, 16, 10, 20]
            ),
        )

    def test__dotcross(self):
        self.assertEqual("+..", Teleprinter.dotcross([1, 0, 0]))

        self.assertEqual(".++..", Teleprinter.dotcross([0, 1, 1, 0, 0]))

        self.assertEqual(
            "+..++.++.", Teleprinter.dotcross([1, 0, 0, 1, 1, 0, 1, 1, 0])
        )

        self.assertEqual(
            "++..+++.....+..",
            Teleprinter.dotcross(
                [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]
            ),
        )

        self.assertEqual(
            "..+...+++++++++++.",
            Teleprinter.dotcross(
                [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
            ),
        )

    def test__binarify(self):
        self.assertEqual([1, 0, 0], Teleprinter.binarify("+.."))

        self.assertEqual([0, 1, 1, 0, 0], Teleprinter.binarify(".++.."))

        self.assertEqual(
            [1, 0, 0, 1, 1, 0, 1, 1, 0], Teleprinter.binarify("+..++.++.")
        )

        self.assertEqual(
            [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            Teleprinter.binarify("++..+++.....+.."),
        )

        self.assertEqual(
            [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            Teleprinter.binarify("..+...+++++++++++."),
        )
