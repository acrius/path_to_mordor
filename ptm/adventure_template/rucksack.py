"""
Module contains settings of adventure.
"""
from os.path import dirname, abspath, join

#Project path.
ADVENTURE_PATH = dirname(abspath(__file__))

#Travels path,
TRAVELS_PATH = join(ADVENTURE_PATH, 'travels')

#Treasy path.
TREASY_PATH = join(ADVENTURE_PATH, 'treasy')

#The maximum number of running browsers.
MAX_CONCURRENT_STEPS = 4

#Waiting time between grab for browser for geting page text.
WAIT_TIME = 0.5

#Name of function for run travel.
RUN_FUNCTION_NAME = 'run'
