from argparse import ArgumentParser
from os import getcwd

from spells import spell_recipes
from ..ptm_settings import PACKAGE_PATH, PROJECT_TEMPLATE_PATH, TRAVEL_TEMPLATE

def parse_args(spell_type):
    parser = _create_argparse(spell_type)
    return parse.parse_args()

def _create_argparse(spell_type):
    parser = ArgumentParser(description='Character for adventure managment.(Adventure is "path_to_mordor" project)')
    for spell_recipe in spell_recipes:
        subparsers = parser.add_subparsers()
        subparser = subparsers.add_parser(spell_recipe.name)
        for ingredient in spell_recipe.ingredients:
            subparser.add_argument(ingredient.synonyms, type=ingredient.type, help=ingredient.description)
        subparser.set_defaults(which=spell_recipe.name)


def collect_spells(rucksack, spell_type):
    args = parse_args(spell_type)
    current_path = getcwd()
    for spell_recipe in spell_recipes:
        if args.which == spell_recipe.name:
            spell_recipe.execute(current_path, rucksack, args)
