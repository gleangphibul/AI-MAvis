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
import sys
import itertools
import numpy as np
from utils import pos_add, pos_sub, APPROX_INFINITY
from collections import deque, defaultdict

import domains.hospital.state as h_state
import domains.hospital.goal_description as h_goal_description
import domains.hospital.level as h_level


class HospitalZeroHeuristic:
    def __init__(self):
        pass

    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior 
        # to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

    def h(self, state: h_state.HospitalState, 
                goal_description: h_goal_description.HospitalGoalDescription) -> int:
        return 0
    

class HospitalGoalCountHeuristics:

    def __init__(self):
        pass
        #raise NotImplementedError()


    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior 
        # to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        
        pass
       #raise NotImplementedError()
    
    def h(self, state: h_state.HospitalState,goal_description: h_goal_description.HospitalGoalDescription) -> int:
        remaining_goals = 0
        for goal in goal_description.agent_goals:
            pos=state.agent_at(goal[0])
            if pos==-1 or pos[1]!=goal[1]:
                remaining_goals+=1
        for goal in goal_description.box_goals:
            pos=state.box_at(goal[0])
            if pos==-1 or pos[1]!=goal[1]:
                remaining_goals+=1
        return remaining_goals

class HospitalAdvancedHeuristics:

    def __init__(self):
        pass
        

    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

   
    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        agent_box_index=0
        positions=state.agent_positions+state.box_positions
        h=0
        for goal in goal_description.goals:
            goal_id=goal[1]
            goal_location=goal[0]
            current_location=positions[agent_box_index][0]
            h=h+(abs(goal_location[0]-current_location[0])+abs(goal_location[1]-current_location[1]))
            agent_box_index=agent_box_index+1
        print("Heuristic value: ",h)
        return h/len(positions)
