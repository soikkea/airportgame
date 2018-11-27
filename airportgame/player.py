"""Relating to the player."""
# -*- coding: utf-8 -*-

class Player():
    """
    Class representing the player
    """

    def __init__(self, name):
        """
        Params:
        name:    str
        """
        self.name = name

    def get_name(self):
        """
        Returns the name of the player.
        Return:    str
        """
        return self.name
