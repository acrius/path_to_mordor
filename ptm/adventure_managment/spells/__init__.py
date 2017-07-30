"""
The module contains Spell class.

The `Spell` describes the `Adventure` controll command.
Based on the objects of `Spells`, an object `Argparse` is built
that provides a command-line interface.
For the construction of `Argpars`, `Spells` are taken from:
     - `ptm.adventure_managment.spells.implementations.spells` - list of define `Spells`;
     - `rucksack.ARTIFACTS.spells` - adventure extensions `Spells`.
"""
from os import getcwd
from collections import namedtuple

from .recipe import Recipe

from .types import GLOBAL_SPELL, LOCAL_SPELL


class Spell:
    """
    The `Spell` describes the `Adventure` controll command.

    Based on the spell, the `Subparser` object is constructed.
    Thus, in one command only one spell can be performed.

        :param name: name of `Spell`. Used as the name of the `Subparser`.
        :param description: description of `Spell`. Used as the help string of command.
        :param recipe: object of `Recipe` of `Spell`.
                       More information about `Recipe` is located
                                                        `ptm.adventure_managment.spells.recipe`.

    Fields rucksack, type and adventure_path declareted in __init__.
    """
    name = 'spell'
    description = ''
    recipe = None

    def __init__(self, rucksack=None):
        """
        Create `Spell` object and determinate its type and secondary parametrs.

        :param rucksack: `Rucksack` of `Adventure`. More information about
                         `Rucksack` of `Adventure` is located
                                    in `ptm.templates.adventure_template.rucksack`.

        If __init__ is not redifined:
            :param type: type of `Spell`.
                If `rucksack` is not None then type is LOCAL_SPELL else GLOBAL_SPELL.
                More information of `Spell types` is located
                in `ptm.adventure_managment.spells.types`.

            :param adventure_path: path of `Adventure` where `Spell` is execute.
                If rucksack is not None and rucksack contains ADVENTURE_PATH
                then adventure path taken from rucksack,
                else adveture path taken from path where command is execute.
        """
        self.rucksack = rucksack
        self.type = (rucksack and LOCAL_SPELL) or GLOBAL_SPELL
        self.adventure_path = self._get_adventure_path()

    def __repr__(self):
        return '{} with recipe: {}'.format(self.name, self.recipe)

    def _get_adventure_path(self):
        return self.rucksack.ADVENTURE_PATH if self.rucksack \
                and hasattr(self.rucksackm 'ADVENTURE_PATH') else getcwd()

    def execute(self):
        """`Spell` execute."""

        #Spell casting is here.
        pass
