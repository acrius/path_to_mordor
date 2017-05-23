"""
Module to manage and run adventure.
"""
from ptm.adventure_managment import execute_spell
from ptm.adventure_managment.spells.types import GLOBAL_SPELL


def execute():
    execute_spell(GLOBAL_SPELL)


if __name__ == '__main__':
    execute()
