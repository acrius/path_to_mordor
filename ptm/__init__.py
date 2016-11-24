#pylint: disable-msg=C0103
"""
Module contains classes to scraping.
"""
from time import sleep
from re import match
from concurrent import futures

from bs4 import BeautifulSoup
from selenium.webdriver import PhantomJS

"""
                                            Frodo.
==================================================================================================
"""
class Frodo:
    """
    Class performs scraping.
    """
    def __init__(self, start_page_url, path, rucksack, wait_render=False):
        """
        Initial.
        Input:
            start_page_url -> Url of start page to scraping;
            path -> Path of scraping;
            ruksack -> Rucksack of Frodo; (Scraping settings);
        """
        self.max_concurrent_steps = rucksack.MAX_CONCURRENT_STEPS
        self.wait_time = rucksack.WAIT_TIME
        self.wait_render = wait_render
        self.render_wait_time = rucksack.RENDER_WAIT_TIME
        self.current_concurrent_steps = 0

        self.start_page_url = start_page_url
        self.resource = self.get_resource(start_page_url)
        self._start_steps = self._create_steps(path)


    @staticmethod
    def _get_resource(url):
        return match(r'^http[s]?://.*\.\w{1,3}/', url).group(0)

    """
                                            Get region.
    ==============================================================================================
    Region is a text of html page.
    """
    def get_region(self, url):
        """
        Get page of text from url.
        Input:
            url -> Url address of page;
        Output:
            page_text -> Source text of html page;
        """
        self._grab_region()
        browser = PhantomJS()
        browser.set_window_size(1440, 900)
        print('Get url: ', url)
        browser.get(url)
        begin_page_text = browser.page_source
        self._release_region()
        if self.wait_render and begin_page_text == browser.page_source:
            sleep(self.render_wait_time)
        page_text = browser.page_source
        browser.close()
        return page_text

    def _grab_region(self):
        """
        Wait one's turn.
        Increase counter self.current_concurrent_steps with grab.
        """
        while self.current_concurrent_steps >= self.max_concurrent_steps:
            sleep(self.wait_time)
        self.current_concurrent_steps += 1

    def _release_region(self):
        """
        Release region.
        """
        self.current_concurrent_steps -= 1


    """
                                            Create steps.
    ==============================================================================================
    """
    def _create_steps(self, path):
        """
        Create lists of steps.
        """
        steps = []
        for action, next_step in path.items():
            steps.append(Step(action,
                              self._create_steps(next_step) if isinstance(next_step, dict)
                              else [Step(next_step, [])]))
        return steps

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

class Step: #pylint: disable-msg=R0903
    """
    Class for describing step of scraping,
    """
    def __init__(self, current_action, next_steps=None):
        self.current_action = current_action
        self.next_steps = next_steps or []

    def  __str__(self):
        return '(Current action: {}, Next step: {})'.format(self.current_action, self.next_steps)

    def  __repr__(self):
        return '(Current action: {}, Next step: {})'.format(self.current_action, self.next_steps)
