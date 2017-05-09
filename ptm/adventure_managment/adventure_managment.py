"""
The module contains functions for project managment.
Project pattern stored in adventure_template package.
The path_to_mordor project is called adventure.
Adventure structure:
    gendalf.py -> The module contains an interface to manage the adventure;
    rucksack.py -> The module contains the settings of adventure;
    treasy -> The package contains the functions to work with output data,
               like as work with database or csv tables;
    trevels -> The package contains groups of travels and travels.
               Travels is scraping rules;
Called functions:
    parse_args -> Parse teminal args;
    start_adventure -> Called the galandriel script to create adventure;
    execute_spell -> Called the gendalf.py script to manage and run adventure;
"""
from os import getcwd, makedirs, listdir
from os.path import basename, splitext, exists, isdir, join
from sys import path
from shutil import copytree, copy2
from argparse import ArgumentParser
from importlib import machinery

from .ptm_settings import PACKAGE_PATH, PROJECT_TEMPLATE_PATH, TRAVEl_TEMPLATE #pylint: disable-msg=E0401,C0301

"""
                                        Parse teminal args.
==================================================================================================
"""
def parse_args(file_path):
    """
    Parse teminal args.
    Use argparse to parsing.
    Input:
        file_path -> Path to executable script;
    """
    parser = _create_argparse(file_path)
    return parser.parse_args()

def _create_argparse(file_path):
    """
    Factory to create argparse object.
    Argparse object is created to galandriel and gendalf.
    Galandriel spells:
        -sa, --start_adventure:(str) -> Create new adventure;
    Gendalf spells:
        -ct, --create_travel:(str) -> Create travel.
        -cl, --create_land:(str) -> Create land.
    Input:
        file_path -> Path to executable file;
    Output:
        parser -> Argparse object;
    """
    character_name = splitext(basename(file_path))[0]
    parser = ArgumentParser()
    if character_name == 'galandriel':
        parser.add_argument('-sa', '--start_adventure', type=str,
                            help='Command to create "path_to_mordor" project.')
    if character_name == 'gendalf' or character_name == 'galandriel':
        parser.add_argument('-cl', '--create_land', type=str,
                            help='Command to create land.')
        parser.add_argument('-ct', '--create_travel', type=str,
                            help='Command to create new travel.')
        parser.add_argument('-r', '--run', type=str,
                            help='Command to run travels')
    return parser


"""
==================================================================================================
"""
def collect_spells(work_dir):
    return spells

"""
                                          (Galandriel)
                                       Start new adveture.
==================================================================================================
"""
def start_adventure(current_path, adventure_name):
    """
    Create adventure.
    In the current_path directory create adventure_name directory.
    In adventure_name directory create adventure from adventure template.
    Input:
        current_path -> path of call a script;
        adventure_name -> name of new adventure;
    """
    #Create path of new adventure.
    adventure_path = join(current_path, adventure_name)

    #If adventure_name directory not exist then create it.
    if not exists(adventure_path) or not isdir(adventure_path):
        makedirs(adventure_path)

    #Create new adventure from adventure template.
    adventure_template_path = join(PACKAGE_PATH, PROJECT_TEMPLATE_PATH)
    _create_adventure(adventure_path, adventure_template_path)


def _create_adventure(adventure_path, adventure_template_path):
    """
    Create new adventure in adventure_path from adventure tamplate in adventure_template_path.
    Input:
        adventure_path -> Path to new adventure;
        adventure_template_path -> Path with adventure template;
    """
    for template_path in listdir(adventure_template_path):
        absolute_template_path = join(adventure_template_path, template_path)
        absolute_adventure_path = join(adventure_path, template_path)
        _copy_template(absolute_template_path, absolute_adventure_path)

def _copy_template(absolute_template_path, absolute_adventure_path):
    """
    Copy template file or dir from absolute_template_path in absolute_adventure_path.
    If absolute_adventure_path is exist then don't copy template.
    Input:
        absolute_template_path -> Path with template dir or file;
        absolute_adventure_path -> Path to new dir or filr;
    """
    if not exists(absolute_adventure_path):
        if isdir(absolute_template_path):
            copytree(absolute_template_path, absolute_adventure_path)
        else:
            copy2(absolute_template_path, absolute_adventure_path)


"""
                                             (Gendalf)
                                           Execute spell.
==================================================================================================
"""
def execute_spell(rucksack, file_path):
    """
    Execute spell from gendalf.py. Spell is a command from script args.
    Spells:
        -ct, --create_travel -> Create travel. Travel is scraping rule.
                                Travel is module with activate function.
                                Activate function is defined in the rucksack of adventure.
                                Example 'python3 gendalf.py --create_travel wiki_travel';
        -cl, --create_land -> Create land. Land is a group of travels.
                              Land is a package with travels modules.
                              Example 'python3 gendalf.py --create_land wiki';
    Input:
        rucksack -> Module with adventure settings;
        file_path -> Path to gendalf.py;
    """
    path.append(rucksack.ADVENTURE_PATH)
    args = parse_args(file_path)
    if args.create_land:
        _create_land(rucksack.TRAVELS_PATH, args.create_land)
    if args.create_travel:
        _create_travel(rucksack.TRAVELS_PATH, args.create_travel)
    if args.run:
        _run_adventure(rucksack, args.run)

def _create_land(travels_path, land_name):
    """
    Create land. Land is a package with travels of adventure.
    Input:
        adventure_path -> Path of adventure;
        land_name -> Name of land;
    """
    land_path = join(travels_path, land_name)
    _make_package(land_path)

def _make_package(package_path):
    """
    Create python package with package_path path.
    Input:
        package_path -> Path of new package;
    """
    if not exists(package_path) or not isdir(package_path):
        makedirs(package_path)
        init_path = join(package_path, '__init__.py')
        _make_module(init_path)

def _create_travel(travels_path, travel_name):
    """
    Create travel. Travel is a module with scaripng rule and activate function.
    Input:
        adventure_path -> Path od adventure;
        travel_name -> Path of new travel;
    """
    travel_path = join(travels_path, '{}.py'.format(travel_name))
    copy2(TRAVEl_TEMPLATE, travel_path)

def _make_module(module_path):
    """
    Create python module.
    Input:
        module_path -> Path of new module;
    """
    if not exists(module_path):
        with open(module_path, 'w+'):
            pass

def _run_adventure(rucksack, travels_string):
    """
    Run adventure. Run all travels from args.
    Input:
        rucksack -> Module with adventure settings;
        travels_string -> String with lands and travels for run;
    """
    if travels_string == 'all':
        _run(rucksack, rucksack.TRAVELS_PATH)
    else:
        travels = travels_string.split(',')
        if travels:
            for travel in travels:
                _run(rucksack, join(rucksack.ADVENTURE_PATH, travel))

def _run(rucksack, travel_path):
    """
    Run travels or land.
    """
    if isdir(travel_path):
        for travel_file in listdir(travel_path):
            _run(rucksack, join(travel_path, travel_file))
    elif travel_path.endswith('.py') and not travel_path.endswith('__init__.py'):
        print("Begin to import module %s.", travel_path)
        travel = machinery.SourceFileLoader('travel', travel_path).load_module()
        print('Finish to import modile %s.', travel_path)
        if rucksack.RUN_FUNCTION_NAME in travel.__dict__.keys():
            travel.__dict__[rucksack.RUN_FUNCTION_NAME](rucksack)
