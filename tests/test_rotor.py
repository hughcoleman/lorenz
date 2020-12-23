#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_rotor.py
# Copyright (c) 2020 Hugh Coleman
#
# This file is part of hughcoleman/lorenz, a historically accurate simulator of
# the Lorenz SZ40 Cipher Machine. It is released under the MIT License (see
# LICENSE.)
import unittest

from lorenz.patterns import ZMUG_CAMS
from lorenz.rotor import MotorSet
from lorenz.rotor import Rotor
from lorenz.rotor import RotorSet


class TestRotor(unittest.TestCase):
    def test__instantiate(self):
        Rotor(ZMUG_CAMS["chi"][0])

    def test__instantiate_invalid(self):
        self.assertRaises(ValueError, Rotor, [0, 1, 0, 2, 1, 1, "x"])

        self.assertRaises(ValueError, Rotor, ZMUG_CAMS["psi"][0], position=-2)

        self.assertRaises(ValueError, Rotor, ZMUG_CAMS["psi"][0], position=100)


class TestRotorSet(unittest.TestCase):
    def test__instantiate(self):
        RotorSet(ZMUG_CAMS["chi"])

    def test__instantiate_invalid(self):
        self.assertRaises(ValueError, RotorSet, ["a", "b", "c", "d", "e"])

        self.assertRaises(
            ValueError,
            RotorSet,
            ZMUG_CAMS["chi"],
            positions=[1, 2, 3, 4, 5, 6],
        )

        self.assertRaises(
            ValueError,
            RotorSet,
            ZMUG_CAMS["chi"],
            positions=[100, 100, 100, 100, 100],
        )

    def test__step(self):
        rotors = RotorSet(ZMUG_CAMS["chi"], positions=[3, 17, 2, 19, 5])

        # if we step the rotors about a thousand times, and they're still in
        # the right places, then it's *probably* fine.
        for _ in range(1024):
            rotors.step()

        self.assertEqual(
            [2, 18, 11, 3, 17], [rotor.position for rotor in rotors.rotors]
        )

    def test__state(self):
        rotors = RotorSet(ZMUG_CAMS["chi"], positions=[3, 17, 2, 19, 5])

        # if it works a few times, it's probably fine.
        for i in range(16):
            self.assertEqual(
                [7, 27, 17, 4, 6, 8, 27, 18, 5, 31, 25, 2, 0, 20, 14, 15][i],
                rotors.state(),
            )

            rotors.step()


class TestMotorSet(unittest.TestCase):
    def test__instantiate(self):
        MotorSet(ZMUG_CAMS["mu"])

    def test__instantiate_invalid(self):
        self.assertRaises(ValueError, MotorSet, ["a", "b"])

        self.assertRaises(
            ValueError, MotorSet, ZMUG_CAMS["mu"], positions=[1, 2, 3]
        )

        self.assertRaises(
            ValueError, MotorSet, ZMUG_CAMS["mu"], positions=[100, 100]
        )

    def test__step(self):
        rotors = MotorSet(ZMUG_CAMS["mu"], positions=[21, 18])

        # if we step the rotors about a thousand times, and they're still in
        # the right places, then it's *probably* fine.
        for _ in range(1024):
            rotors.step()

        self.assertEqual([8, 3], [rotor.position for rotor in rotors.rotors])

    def test__state(self):
        rotors = MotorSet(ZMUG_CAMS["mu"], positions=[57, 28])

        # if it works a few times, it's probably fine.
        for i in range(16):
            self.assertEqual(
                [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0][i],
                rotors.state(),
            )

            rotors.step()
