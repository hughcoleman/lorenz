#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rotor.py
# Copyright (c) 2020 Hugh Coleman
#
# This file is part of hughcoleman/lorenz, a historically accurate simulator of
# the Lorenz SZ40 Cipher Machine. It is released under the MIT License (see
# LICENSE.)
""" Implements `Rotor`, `RotorSet`, and `MotorSet` classes for easier handling
of the rotors and rotor groups in the Lorenz machine.

These types can be combined in unique ways to create "customized" versions of
the Lorenz machine.
"""


class Rotor:
    """ Emulate a single rotor. """

    def step(self):
        """ Step the rotor forwards. """
        self.position = (self.position + 1) % len(self.pins)

    def backstep(self):
        """ Step the rotor backwards. """
        self.position = (self.position - 1) % len(self.pins)

    def state(self):
        """ Get the active bit of this rotor. """
        return self.pins[self.position]

    def __init__(self, pins, position=0):
        """Create a Rotor.

        pins
            Provide a list of bits representing the positions of the cams/pins
            on the rotor.

                0 = lowered
                1 = raised

            For maximum cryptographic strength, rotor cams should be selected
            such that they are made up of apprixmately equal numbers of raised
            and lowered cams. In addition, cam positions should be selected
            such that the delta stream produced by said rotor also contains an
            approixmately equal distribution of zeroes and ones.

        position
            Specify the initial position of the rotor.

            If specified, the "active" position of this rotor is set to the
            given value. If empty, a zero start position is inferred.
        """

        if any(bit not in [0, 1] for bit in pins):
            raise ValueError("cannot set rotor using non-binary cam position.")

        if (position < 0) or (position > len(pins)):
            raise ValueError(f"illegal rotor start position {position}.")

        self.pins = pins
        self.position = position


class RotorSet:
    """Emulate a set of synchronized rotors. When stepped, all rotors in the
    set will step simultaneously.

    The Chi and Psi rotors are examples of RotorSets.
    """

    def step(self):
        """ Step the RotorSet forwards. """
        for rotor in self.rotors:
            rotor.step()

    def backstep(self):
        """ Step the RotorSet backwards. """
        for rotor in self.rotors:
            rotor.step()

    def state(self):
        """Return an n-bit (n being the number of rotors in this RotorSet)
        integer, based on the states of the rotors in this RotorSet.

        The most significant bit of this integer will correspond to the state
        of the first rotor in the set, and so on, all the way down to the least
        significant bit corresponding the state of the last rotor in the set.
        """

        state = 0
        for rotor in self.rotors:
            state = (state << 1) | rotor.state()
        return state

    def sizes(self):
        """ Get the sizes of the rotors in this RotorSet. """
        return [len(rotor) for rotor in self.rotors]

    def __init__(self, rotors, positions=None):
        """Create a RotorSet.

        rotors
            Specify the rotors with which to constuct this RotorSet. This must
            be a list, containing either:

                (a) An ordered list of `Rotor` instances; or
                (b) An ordered list of lists; each sub-list representing the
                    cam positions on said Rotor. These will internally be
                    converted to Rotor instances and as such must satisfy the
                    constraints for the `pins` parameter of Rotor.__init__().

        positions
            Specify the starting positions of the rotors in this RotorSet. This
            must be a list of integers, equal in length to `rotors`.

            Each integer should specify the starting position of the rotor in
            the same index position in the `rotors` parameter. If left empty,
            the set is initialized to the all-zero state.

            * this parameter is ignored if a list of Rotor instances is passed
            to the `rotor` parameter of this class' constructor.
        """

        if all(type(rotor) is Rotor for rotor in rotors):
            self.rotors = rotors

        elif all(type(rotor) is list for rotor in rotors):
            if positions is None:
                positions = [0] * len(rotors)

            if len(rotors) != len(positions):
                raise ValueError("mismatched rotors and positions")

            self.rotors = [
                Rotor(rotor, position)
                for rotor, position in zip(rotors, positions)
            ]

        else:
            raise ValueError("illegal parameters.")


class MotorSet:
    """Emulate a set of staggered rotors.

    When stepped, the rotors in this MotorSet step in a "staggered" fashion. In
    general, the state of the nth rotor in a MotorSet determines if the n+1th
    rotor steps.

    The Mu rotors are an example of a MotorSet.
    """

    def step(self):
        """ Step the MotorSet forwards. """
        for i in range(len(self.rotors) - 1, -1, -1):
            if i == 0:
                self.rotors[i].step()
            else:
                if self.rotors[i - 1].state():
                    self.rotors[i].step()

    def backstep(self):
        """ Step the MotorSet backwards. """
        flag = True
        for rotor in self.rotors:
            if flag:
                rotor.backstep()
            flag = bool(rotor.state())

    def state(self):
        """ Get the state of the MotorSet. """
        return self.rotors[-1].state()

    def sizes(self):
        """ Get the sizes of the rotors in this MotorSet. """
        return [len(rotor) for rotor in self.rotors]

    def __init__(self, rotors, positions=None):
        """Create a MotorSet.

        rotors
            Specify the rotors with which to constuct this MotorSet. This must
            be a list, containing either:

                (a) An ordered list of `Rotor` instances; or
                (b) An ordered list of lists; each sub-list representing the
                    cam positions on said Rotor. These will internally be
                    converted to Rotor instances and as such must satisfy the
                    constraints for the `pins` parameter of Rotor.__init__().

        positions
            Specify the starting positions of the rotors in this MotorSet. This
            must be a list of integers, equal in length to `rotors`.

            Each integer should specify the starting position of the rotor in
            the same index position in the `rotors` parameter. If left empty,
            the set is initialized to the all-zero state.

            * this parameter is ignored if a list of Rotor instances is passed
            to the `rotor` parameter of this class' constructor.
        """

        if all(type(rotor) is Rotor for rotor in rotors):
            self.rotors = rotors

        elif all(type(rotor) is list for rotor in rotors):
            if positions is None:
                positions = [0] * len(rotors)

            if len(rotors) != len(positions):
                raise ValueError("mismatched rotors and positions")

            self.rotors = [
                Rotor(rotor, position)
                for rotor, position in zip(rotors, positions)
            ]

        else:
            raise ValueError("illegal parameters.")
