'''
Module contains spell and recipe for create travel. Travel is python module
containing rules for scrapping.
'''
from os.path import join

from . import Spell
from .recipe import Recipe, Ingredient
from .types import LOCAL_SPELL

from ...ptm_settings import TRAVEL_TEMPLATE


class CreateTravel:
    name = 'create_travel'
    description = '''Create travel. Travel is a python module
                          containing scrapping rules.'''
    type = LOCAL_SPELL

    recipe = Recipe(Ingredient(synonyms=['name', ], type=str, description='Name of travel.'),
                    Ingredient(synonyms=['-l', '--land'], type=str,
                               description='Land of travel.', default=''))

    def execute(self):
        land_path = self.recipe.land or ''
        travel_path = join(join(land, self.rucksack.TRAVELS_PATH), '{}.py'.format(self.recipe.name))
        copy2(TRAVEL_TEMPLATE, travel_path)
