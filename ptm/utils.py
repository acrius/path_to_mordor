from importlib import machinery
from os.path import join

from collections import Iterable

from ptm_settings import PROJECT_TEMPLATE_PATH


def get_standart_rucksack():
    return machinery.SourceFileLoader('rucksack', join(PROJECT_TEMPLATE_PATH, 'rucksack.py'))\
                    .load_module()


def deep_unpack_items(items):
    unpacked_items, iterable_items = _get_items(items)
    while iterable_items:
        unpacked_subitems, iterable_items = _unpack_items(iterable_items)
        unpacked_items.append(unpacked_subitems)
    return unpacked_items


def _get_items(items):
    unpacked_items = []
    iterable_items = []
    for item in items:
        if isinstance(item, Iterable):
            iterable_items.append(item)
        else:
            unpacked_items.append(item)
    return unpacked_items, iterable_items


def _unpack_items(items):
    unpacked_items, iterable_items = _get_items(items)
    for item in iterable_items:

    return unpacked_items, iterable_items


def _unpack_item(item):
    return
    if isinstance(item, Iterable):
        unpacked_subitems, iterable_subitems = _get_items(subitem for subitem in item)
        unpacked_items.extend(unpacked_subitems)
        iterable_items.extend(iterable_items)
    else:
        unpacked_items.append(item)
