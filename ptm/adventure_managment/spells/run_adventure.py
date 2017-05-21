'''
Module contains spell and recipe for run adventure.
'''
from importlib import machinery
from os import listdir
from os.path import join

from . import Spell
from .recipe import Recipe, Ingredient
from .utils import apply
from .types import LOCAL_SPELL
from ... import Habbit


class RunAdventure:
    name = 'run'
    description = 'Run travels of adventure'
    type = LOCAL_SPELL
    recipe = Recipe(
        Ingredient(synonyms=['-t', '--travels'], type=str, description='Name of travel.'),
        Ingredient(synonyms=['-l', '--lands'], type=str, description='Name of land.'),
        Ingredient(synonyms=['-b', '--brotherhoods'], type=str,
                   description='Name of brotherhoods.'))

    def execute(self):
        self.travels = self.recipe.travels and self.recipe.travels.split(',')
        self.brotherhoods = self.recipe.brotherhoods and self.recipe.brotherhoods.split(',')
        apply(lambda land: self._run(land), self._get_lands())

    def _get_lands(self):
        return self.recipe.lands.split(',') if self.recipe.lands else self.rucksack.TRAVEL_PATH

    def _run(self, travel_path):
        """
        Run travels or land.
        """
        if isdir(travel_path):
            apply(lambda travel_file: self._run(travel_file), listdir(travel_path))
        elif travel_path.endswith('.py') and not travel_path.endswith('__init__.py'):
            self._run_travel(machinery.SourceFileLoader('travel', travel_path).load_module())

    def _run_travel(self, travel):
        if (not self.brotherhoods) or ((self.brotherhoods and 'BROTHERHOODS' in travel.__dict__)
                                       and self.brotherhoods.issubset(travel.BROTHERHOODS)):
            apply(lambda habbit: _run_habbit(habbit, rucksack), _get_habbits(travel))

    @staticmethod
    def _get_habbits(travel):
        return filter(lambda part: isinstance(part, Habbit), travel.__dict__.values())

    def _run_habbit(self, habbit):
        frodo = habbit(self.rucksack)
        frodo.run()
