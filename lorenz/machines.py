#!/usr/bin/env python
# -*- coding: utf-8 -*-
# machines.py
# Copyright (c) 2020 Hugh Coleman
#
# This file is part of hughcoleman/lorenz, a historically accurate simulator of
# the Lorenz SZ40 Cipher Machine. It is released under the MIT License (see
# LICENSE.)
""" A historically-accurate implementation of the Lorenz SZ-40 machine.

The RotorSet and MotorSet classes are abstracted upon to create an emulator for
this machine.

A beginner-friendly explanation of this specific machine can be found on the
following Wikipedia articles:
 - https://en.wikipedia.org/wiki/Lorenz_cipher
 - https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Lorenz_cipher

"""
from lorenz.rotor import MotorSet
from lorenz.rotor import Rotor
from lorenz.rotor import RotorSet


class SZ40:
    """ A historically-accurate implementation of the Lorenz SZ-40 machine. """

    def step(self):
        """ Step the machine's rotors one position forward. """
        if self.mu.state():
            self.psi.step()
        self.mu.step()
        self.chi.step()

    def backstep(self):
        """ Step the machine's rotors one position backward. """
        self.chi.backstep()
        self.mu.backstep()
        if self.mu.state():
            self.psi.backstep()

    def state(self):
        """Return the pseudorandom value in the active position(s) of the
        Chi and Psi rotors.
        """

        return self.chi.state() ^ self.psi.state()

    def feed(self, stream):
        """Feed a stream of information into the machine, using Lorenz
        to generate the key.

        Each character in the input stream is XOR'ed with the current state of
        the Lorenz machine, then the machine is stepped one position.
        """

        output = []
        for word in stream:
            if (type(word) is not int) or (word < 0) or (word >= 32):
                raise RuntimeError(f'illegal word "{word}" in stream.')

            output.append(word ^ self.state())
            self.step()

        return output

    def __init__(self, rotors, positions=None):
        """Create a Lorenz SZ-40 machine.

        rotors
            Specify the rotor settings with which to construct this machine
            using a dictionary with three keys: `chi`, `psi`, and `mu`.

        positions
            Specify the initial rotor positions using a dictionary with three
            keys: `chi`, `psi`, and `mu`.
        """

        if positions is None:
            self.chi = RotorSet(rotors["chi"])
            self.psi = RotorSet(rotors["psi"])
            self.mu = MotorSet(rotors["mu"])
        else:
            self.chi = RotorSet(rotors["chi"], positions=positions["chi"])
            self.psi = RotorSet(rotors["psi"], positions=positions["psi"])
            self.mu = MotorSet(rotors["mu"], positions=positions["mu"])
