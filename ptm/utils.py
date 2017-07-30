from importlib import machinery
from path import join

from ptm_settings import PROJECT_TEMPLATE_PATH


def get_standart_rucksack():
    return machinery.SourceFileLoader('rucksack', join(PROJECT_TEMPLATE_PATH, 'rucksack.py'))\
                    .load_module()
