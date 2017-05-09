"""

"""
from collections import namedtuple
from os.path import join

from .types import GLOBAL_SPELL, LOCAL_SPELL

'''
                                       Spell and Spell Recipe.
==================================================================================================
**Spell** is function to perform a conversion with an adventure("path_to_mordor" project).
**SpellRecipe** is class to describing the call of the spell.
**Ingredient** is class to describing the ingredients for spell.
This data is needed to build command-line parser data.
The RecipeSpell is used as a parser of subparsers.
The Ingredient is used as an argument of a parser based on a SpellRecipe.
The functions of the spell are passed arguments:
    :param current_path: the path where the script was run;
    :param rucksack: module with adventure settings;
    :param ingredients: value of ingredients of spell;
    :type current_path: str
    :type rucksack: module or tuple
    :type ingredients: dict
'''
#Create Ingredient class how namedtuple.
Ingredient = namedtuple('Ingredient', [('synonyms', List[str]), 'type', ('description', str)])
#SpellRecipe fields
spell_fields = [('name', str), 'type', ('description', str), 'execute']
recipe_fields = ['ingredients', **spell_fields]
#Create SpellRecipe class how namedtuple.
SpellRecipe = namedtuple('SpellRecipe', recipe_fields)


'''
                                           Start adventure.
==================================================================================================
'''
#TODO: refactor start adventure spell and supporting functions,
def start_adventure(current_path: str, rucksack, ingredients: dict):
    '''
    Create adventure.
    In the adventure_path directory create adventure_name directory.
    In adventure_name directory create adventure from adventure template.
        :param current_path: path of call a script;
        :param rucksack: name of new adventure;
        :param ingredients: ingredients of spell;
        :type current_path: string
        :type rucksack: module
        :type ingredients: dict
    '''
    #Create path of new adventure.
    adventure_path = _get_adventure_path(current_path, rucksack, ingredients)

    #If adventure_name directory not exist then create it.
    if not exists(adventure_path) or not isdir(adventure_path):
        makedirs(adventure_path)

    #Create new adventure from adventure template.
    adventure_template_path = join(PACKAGE_PATH, PROJECT_TEMPLATE_PATH)
    _create_adventure(adventure_path, adventure_template_path)

def _get_adventure_path(current_path, rucksack, ingredients):
    '''
    Get adventure path.
        :param current_path: path of call a script;
        :param rucksack: settings of adventure;
        :param ingredients: ingredients of spell;
        :type current_path: string
        :type rucksack: module
        :type ingredients: dict
    '''
    return _get_adventure_path_from_rucksack(rucksack) or
           _get_adventure_path_from_ingredients(current_path, ingredients)

def _get_adventure_path_from_rucksack(rucksack):
    """
    Get adventure path from rucksack(Adventure("path to mordor" project) settings).
        :param rucksack: settings of adventure
        :type rucksack: module or tupple
    """
    return rucksack.ADVENTURE_PATH if rucksack and 'ADVENTURE_PATH' in rucksack.__dict__\
                                   else None

def _get_adventure_path_from_ingredients(current_path, ingredients):
    '''
    Get adventure path from ingredients and current path.
    '''
    return _join_adventure_path(ingredients.name, current_path, ingredients.path)\
           if ingredients.path else join(current_path, ingredients.name)

def _join_adventure_path(adventure_name: str, current_path: str, path: str):
    return join(path, adventure_name) if path.startwith('/')\
           else join(current_path, path, adventure_name)

def _create_adventure(adventure_path: str, adventure_template_path: str):
    '''
    Create new adventure in adventure_path from adventure tamplate in adventure_template_path.
        :param adventure_path: path to new adventure;
        :param adventure_template_path: path with adventure template;
        :type adventure_path: string
        :type adventure_template_path: string
    '''
    for template_path in listdir(adventure_template_path):
        absolute_template_path = join(adventure_template_path, template_path)
        absolute_adventure_path = join(adventure_path, template_path)
        _copy_template(absolute_template_path, absolute_adventure_path)

def _copy_template(absolute_template_path: str, absolute_adventure_path: str):
    '''
    Copy template file or dir from absolute_template_path in absolute_adventure_path.
    If absolute_adventure_path is exist then don't copy template.
        :param absolute_template_path: path with template dir or file;
        :param absolute_adventure_path: path to new dir or file;
        :type absolute_template_path: string
        :type absolute_adventure_path: string
    '''
    if not exists(absolute_adventure_path):
        if isdir(absolute_template_path):
            copytree(absolute_template_path, absolute_adventure_path)
        else:
            copy2(absolute_template_path, absolute_adventure_path)

start_adventure_ingredients = [Ingredient(synonyms=['name',], type=str,
                                          description='Name of adventure.'),
                               Ingredient(synonyms=['-p', '--path'], type=str,
                                          description='Path to adventure')]
start_adventure_recipe = SpellRecipe(name='start_adventure',
                                     type=GLOBAL_SPELL,
                                     execute=start_adventure,
                                     ingredients=start_adventure_ingredients,
                                     description='Create adventure("path_to_mordor" project).')


'''
                                          Create land.
==================================================================================================
'''
def create_land(current_path: str, rucksack, ingredients: dict):
    '''
    Create land. Land is a package with travels of adventure.
        :param current_path: path of call a script;
        :param rucksack: name of new adventure;
        :param ingredients: ingredients of spell;
        :type current_path: string
        :type rucksack: module
        :type ingredients: dict
    '''
    land_path = join(rucksack.TRAVELS_PATH, ingredients.name)
    _make_package(land_path)


create_land_ingredients = [Ingredient(synonyms=['name',], type=str,
                                      description='Name of land.')]
create_land_recipe = SpellRecipe(name='create_land',
                                 type=LOCAL_SPELL,
                                 execute=create_land,
                                 ingredients=create_land_ingredients,
                                 description='''Create land. Land is group of travels.
                                                Travel is python module. Land is a python
                                                package containing modules(travels)
                                                or other python packages(lands).''')


'''
                                          Create travel.
==================================================================================================
'''
def create_travel(current_path: str, rucksack, ingredients: dict):
    '''
    Create travel. Travel is a module with scaripng rule and activate function.
        :param current_path: path of call a script;
        :param rucksack: name of new adventure;
        :param ingredients: ingredients of spell;
        :type current_path: string
        :type rucksack: module
        :type ingredients: dict
    '''
    land_path = ingredients.land or ''
    travel_path = join(join(land, rucksack.TRAVELS_PATH), '{}.py'.format(ingredients.name))
    copy2(TRAVEl_TEMPLATE, travel_path)

create_travel_ingredients = [Ingredient(synonyms=['name',], type=str,
                                        description='Name of travel.'),
                             Ingredient(synonyms=['-l', '--land'], type=str,
                                        description='Land of travel.')]

create_travel_recipe = SpellRecipe(name='create_travel',
                                   type=LOCAL_SPELL,
                                   execute=create_travel,
                                   ingredients=create_travel_ingredients,
                                   description='''Create travel. Travel is a python module
                                                  containing scrapping rules. The input point
                                                  for scraping is a function "run".''')


'''
                                                Run.
==================================================================================================
'''
#TODO refactor and restrcture this spell,
def run_adventure(current_path: str, rucksack, ingredients: dict):
    """
    Run adventure. Run all travels from args.
        :param current_path: path of call a script;
        :param rucksack: name of new adventure;
        :param ingredients: ingredients of spell;
        :type current_path: string
        :type rucksack: module
        :type ingredients: dict
    """
    brotherhoods = ingredients.brotherhood and ingredients.brotherhood.split(',')
    run_function_name = rucksack.RUN_FUNCTION_NAME
    if not (ingredients.travel or ingredients.land):
        _run(rucksack.TRAVELS_PATH, run_function_name, brotherhoods)
    else:
        travels = ingredients.travels.split(',')
        brotherhoods = ingredients.brotherhood.split(',')
        if travels:
            for travel in travels:
                _run(join(rucksack.ADVENTURE_PATH, travel), run_function_name, brotherhoods)

def _run(travel_path, run_function_name, brotherhoods):
    """
    Run travels or land.
    """
    if isdir(travel_path):
        for travel_file in listdir(travel_path):
            _run(rucksack, join(travel_path, travel_file))
    elif travel_path.endswith('.py') and not travel_path.endswith('__init__.py'):
        travel = machinery.SourceFileLoader('travel', travel_path).load_module()
        if run_function_name in travel.__dict__.keys():
            if 'BROTHERHOODS' in travel:
                if [brotherhood for brotherhood in brotherhoods if brotherhood in travel.BROTHERHOODS]:
                    travel.__dict__[run_function_name](rucksack)
            else:
                travel.__dict__[run_function_name](rucksack)

run_adventure_ingredients = [Ingredient(synonyms=['-t', '--travel'], type=str,
                                        description='Name of travel.'),
                             Ingredient(synonyms=['-l', '--land'], type=str,
                                        description='Name of land.'),
                             Ingredient(synonyms=['-b', '--brotherhood'], type=str,
                                        description='Name of brotherhood.')]

run_adventure_recipe = SpellRecipe(name='run',
                                   type=LOCAL_SPELL,
                                   execute=run_adventure,
                                   ingredients=run_adventure_ingredients,
                                   description='Run travels of adventure')

'''
                                         Secondary functions.
==================================================================================================
'''
def _make_package(package_path: str):
    """
    Create python package with package_path path.
        :param package_path: path of new package;
        :type package_path: string
    """
    if not exists(package_path) or not isdir(package_path):
        makedirs(package_path)
        init_path = join(package_path, '__init__.py')
        _make_module(init_path)

def _make_module(module_path: str):
    """
    Create python module.
        :param module_path: path of new module;
        :type module_path: string
    """
    if not exists(module_path):
        with open(module_path, 'w+'):
            pass


'''
                                           List of spell recipes.
==================================================================================================
'''
spell_recipes = (
    start_adventure_recipe,
    create_land_recipe,
    create_travel_recipe,
    run_adventure_recipe
)
