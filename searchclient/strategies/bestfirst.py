# coding: utf-8
#
# Copyright 2021 The Technical University of Denmark
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import heapq
import itertools
import random

import domains.hospital.goal_description as h_goal_description
import domains.hospital.state as h_state

# Here we define a priority queue which allows the priority of elements to be updated in constant time.
# This priority queue is therefore suitable for usage as the frontier in a best-first search.
class PriorityQueue:

    def __init__(self):
        self.heap = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def add(self, element: h_state.HospitalState, priority: int):
        # The elements are stored in a queue as a triplet (priority, count, element)
        # Python sorts tuples by comparing the first position and if these tie progressing to the next position until
        # it either finds a position in the tuples where they differ or all positions has been compared (in which case
        # the two tuples are identical. By storing the priority in the first position, we ensures that the element
        # with the lowest priority will be placed in the front of the queue.
        # The second component is used to break ties when two elements have the same priority.
        # By using a random number for the tie breaker, we ensure that ties are broken at random
        # Note that we can use a counter to achieve LIFO or FIFO tie-breaking mechanisms
        # The entry finder stores a reference to all elements which ensures that we later can access the entry.

        #This becomes a nice nice nice random walk
        tie_breaker = random.random()
        entry = [priority, tie_breaker, element]
        #This becomes BFS (FIFO)
        # count = next(self.counter)
        # entry = [priority, count, element]
        #This is LIFO
        # count = next(self.counter)
        # entry = [priority, -count, element]
        heapq.heappush(self.heap, entry)
        self.entry_finder[element] = entry

    def change_priority(self, element: h_state.HospitalState, new_priority: int):
        # We cannot change the priority of an element already in the heap as that would break the heap invariant.
        # Instead we invalidate the current entry by replacing the element with None and then inserting the element
        # again with the new priority.
        entry = self.entry_finder.pop(element)
        entry[2] = None
        # Add new entry with new priority
        self.add(element, new_priority)

    def pop(self) -> h_state.HospitalState:
        # Since some of the elements in the queue might have been invalidated by the 'change_priority' method, we need
        # to keep taking elements from the queue until we find a valid entry.
        while True:
            entry = heapq.heappop(self.heap)
            if entry[2] is not None:
                break
        state = entry[2]
        self.entry_finder.pop(state)
        return state

    def clear(self):
        self.heap.clear()
        self.entry_finder.clear()
        self.counter = itertools.count()

    def size(self) -> int:
        return len(self.entry_finder)

    def get_priority(self, element) -> int:
        entry = self.entry_finder.get(element)
        if entry is None:
            return None
        return entry[0]

class FrontierBestFirst:

    def __init__(self):
        self.goal_description = None
        self.priority_queue = PriorityQueue()


    def prepare(self, goal_description: h_goal_description.HospitalGoalDescription):
        self.goal_description = goal_description
        # Prepare is called at the beginning of a search and since we will sometimes reuse frontiers for multiple
        # searches, prepares must ensure that state is cleared.
        # Your code here...
        self.priority_queue.clear()
        # raise NotImplementedError()

    def f(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        raise Exception("FrontierBestFirst should not be directly used. Instead use a subclass overriding f()")

    def add(self, state: h_state.HospitalState):
        self.priority_queue.add(state, self.f(state, self.goal_description))
        #raise NotImplementedError()

    def pop(self) -> h_state.HospitalState:
        return self.priority_queue.pop()
        #raise NotImplementedError()

    def is_empty(self) -> bool:
        return self.priority_queue.size() == 0
        #raise NotImplementedError()

    def size(self) -> int:
        return self.priority_queue.size()
        #raise NotImplementedError()

    def contains(self, state: h_state.HospitalState) -> bool:
        if self.priority_queue.get_priority(state) is None:
            return False
        else:
            return True
        #raise NotImplementedError()


# The FrontierAStar and FrontierGreedy classes extend the FrontierBestFirst class, that is, they are
# exact copies of the above class but where the 'f' method is replaced
class FrontierAStar(FrontierBestFirst):

    def __init__(self, heuristic):
        super().__init__()
        self.heuristic = heuristic

    # Returns cost evaluation (f function)
    def f(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        h = self.heuristic.h(state,goal_description)
        g = state.path_cost
        # print(g)
        f = h + g
        return f
        #raise NotImplementedError()
        

class FrontierGreedy(FrontierBestFirst):

    def __init__(self, heuristic):
        super().__init__()
        self.heuristic = heuristic

    # Returns cost evaluation (f function)
    def f(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:

        f = self.heuristic.h(state, self.goal_description)
        return f
        #raise NotImplementedError()
    