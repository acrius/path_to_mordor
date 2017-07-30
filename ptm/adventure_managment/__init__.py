"""
The module contains main functions for managing the scrapping progect.

The project of scrapping is called an *Adventure*.
To manage the *Adventure*, use the command line based on *Argparse*.

The *Adventure* is controlled by *Spells*.
A *Spell* is a special class that controls an *Adventure* according to a given pattern.
From *Spells* an `Argparse` object is build to manage them from command line.
You can use your *Spells* to manage the *Adventure*. To do this, add your *Spells* to
the list of *Spells* in *artifacts of Adventure* module.
More information about the *Spells* can be read in the module `ptm.adventure_managment.spells`.

The *Adventure* template is stored in `ptm.templates.adventure_template`.

The adventure cinsist of the following packages:

    *travels*    - Package responsible for obtaining data. The module contains scrapping rules.
    *treasy*     - Package responsible for storing data.

    *smithy*     - Package responsible for processing data before saving.

    *artifacts*  - Package containing extensions of *Adventure*.

and modules:

    *rucksack*   - Module containing settings of *Adventure*.

    *gendalf*    - Module for controll of *Adventure*.

More information about modules and packages of *Adventure* can be read in them.

Scraping rules in *Adventure* are called *travel*.
*Travel* template is located at ptm.templates.travel_template.
The main class that implementts scrapping is the Habbit class.
More information about scrapping on an *Adventure* can be read in *__init__* module of ptm package.
"""

from argparse import ArgumentParser
from os import getcwd

from .spells.implementations import spells as _spells
from .spells.types import GLOBAL_SPELL
from ..ptm_settings import PACKAGE_PATH, PROJECT_TEMPLATE_PATH, TRAVEL_TEMPLATE


"""
==================================================================================================
                                     Entry point. Execute *Spell*.
==================================================================================================
"""


def execute_spell(spell_type=GLOBAL_SPELL, rucksack=None):
    """
    Execute *spell* from command line.

    The function is exercising control of the *Adventure*.

    The function executes *Spell* specified in the command line using the control script.
        :param spell_type: Used to select needed *Spells* to build Argparse. More information
                           about types of *Spell* in `ptm.adventure_managment.spells.types`.
        :param rucksack:   Rucksack of current *Adventure*. If *spell_type* is *GLOBAL_SPELL*
                           then rucksack's not needed.
    """
    spells = _get_spells(rucksack, spell_type)

    parser = _create_argparse(spells)
    arguments = parser.parse_args()

    if 'Spell' in arguments.__dict__:
        _run_spell(arguments, rucksack)
    else:
        _print_spells(spells)


def _run_spell(arguments, rucksack):
    spell = arguments.Spell(rucksack)
    spell.recipe.set_ingredients_values({key: value for key, value in arguments.__dict__.items()
                                         if key != 'Spell'})
    spell.execute()


def _print_spells(spells):
    print('Select one of spells:')
    for spell in spells:
        print('    * {}'.format(spell.name))


"""
===================================================================================================
                                             Get Spells
===================================================================================================
"""


def _get_spells(rucksack, spell_type):
    """
    Get a list of active *spells*.

    The list consists of standard *spells* and *spells*
    from *artifact* module of *Adventure*. If rucksack is None then *spells* from *artifact* module
    can not be obtained. *Spells* are selected by type.
    """
    return [Spell for Spell in _spells + _get_artifacts_spells(rucksack)
            if Spell.type == spell_type]


def _get_artifacts_spells(rucksack):
    artifacts = _get_artifacts(rucksack)
    return artifacts and hasattr(artifacts, 'SPELLS') and getattr(artifacts, 'SPELLS') or ()


def _get_artifacts(rucksack):
    return rucksack and hasattr(rucksack, 'ARTIFACTS') and getattr(rucksack, 'ARTIFACTS') or None


"""
===================================================================================================
                            Create *Argparse* object from *Spells* list.
===================================================================================================
"""


def _create_argparse(spells):
    """
    Create *Argparse* object from *Spells* list.

    For each *Spell* from spells, a sub-parser is created.
    Arguments for sub-parses are created from

        :param spells: List of *Spells* objects.
    """
    parser = ArgumentParser(
        description='Character for adventure managment.(Adventure is "path_to_mordor" project)')
    subparsers = parser.add_subparsers()
    for Spell in spells:
        subparser = subparsers.add_parser(Spell.name)
        for ingredient in Spell.recipe:
            subparser.add_argument(
                *ingredient.synonyms, type=ingredient.type, help=ingredient.description)
        subparser.set_defaults(Spell=Spell)
    return parser
