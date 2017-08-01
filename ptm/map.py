'''

'''
from collections import Iterable
from actions import Action


class Sandbox:
    def __init__(self, index, action):
        self.index = index
        self.action = action
        self.is_finish = action.is_finish if hasattr(action, 'is_finish') else False

    def __hash__(self):
        return hash(self.action) ^ hash(self.index)


class Map:
    def __init__(self, *start_actions):
        self.adjacencies = {}
        self.nodes_count = 0

    def to(self, *nodes):
        for node in nodes:
            self._append_layer(node)

    def _append_layer(self, layer):
        if isinstance(layer, Map):
        elif isinstance(layer, Action):
            self._append_node(layer)

    def _append_node(self, node):
        for last_node in self.last_nodes:
            self._append_adjacent_node(last_node, node)
        if not node.is_finish and node not in self.adjacencies.keys():
            self.adjacencies[node] = set()

    def _append_adjacent_node(self, node, adjacent_node):
        self.adjacencies[node].add(adjacent_node)

    @property
    def last_nodes(self):
        return set(node for node, adjacencies in self.adjacencies.items() if adjacencies)

    @property
    def finish_nodes(self):
        return set(node for adjacencies in self.adjacencies.values() for node in adjacencies) - \
               set(self.adjacencies.keys())

    @property
    def start_nodes(self):
        return set(self.adjacencies.keys()) - \
               set(node for adjacencies in self.adjacencies.values() for node in adjacencies)

    def __len__(self):
        return len(self.adjacencies.keys())

def _from(*actions):
    start_actions = actions
    while True:

    return Map(actions)
