"""Module contains classes to scraping."""
from time import sleep
from re import match
from concurrent import futures
import urllib.request
import logging

from bs4 import BeautifulSoup

from .robber import Robber
from .path import Path
from .actions import Action
from .utils import get_standart_rucksack


__version__ = '0.0.1a4'


"""
                                            Habbit.
==================================================================================================
"""


class Habbit:
    """Class performs scraping."""
    start_page_url = ''
    path = {}

    def __init__(self, rucksack=None):
        """
        Initial.
        Input:
            start_page_url -> Url of start page to scraping;
            path -> Path of scraping;
            ruksack -> Rucksack of Habbit; (Scraping settings);
        """
        self.rucksack = rucksack or get_standart_rucksack()
        self._set_resource_from_url(self.start_page_url)
        self._robber = Robber(rucksack)

    def _set_resource_from_url(self, url):
        try:
            self.resource = match(r'^http[s]?://.*\.\w{1,3}', url).group(0)
        except ValueError:
            logging.error(ValueError)

    """
                                            Run adventure.
    ==============================================================================================
    """

    def run(self):
        """
        Run scraping.
        """
        for step in self._start_steps:
            self._make_step(step,
                            (self.start_page_url,
                             BeautifulSoup(self.get_region(self.start_page_url), 'html.parser')))

    def _make_step(self, step, parent):
        """
        Make step.
        """
        for result in step.current_action(self, parent):
            for next_step in step.next_steps:
                self._make_step(next_step, result)


class Step:
    """
    Class for describing step of scraping,
    """
    def __init__(self, current_action, next_steps=None):
        self.current_action = current_action
        self.next_steps = next_steps or []

    def __str__(self):
        return '(Current action: {}, Next step: {})'.format(self.current_action, self.next_steps)

    def __repr__(self):
        return '(Current action: {}, Next step: {})'.format(self.current_action, self.next_steps)
