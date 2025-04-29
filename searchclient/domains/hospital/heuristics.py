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
        h=0

        for goal_pos, goal_idx in goal_description.agent_goals:
            for agent_pos, agent_idx in state.agent_positions:
                if goal_idx == agent_idx:
                   h=h+abs((goal_pos[0]-agent_pos[0])+(abs(goal_pos[1]-agent_pos[1])))
                    
            
        for goal_pos, goal_idx in goal_description.box_goals:
            prior=None
            for box_pos, box_idx in state.box_positions:
                
                if goal_idx == box_idx:
                   distance=abs((goal_pos[0]-box_pos[0])+(abs(goal_pos[1]-box_pos[1])))
                   if prior is None:
                       prior = distance
                   if(distance<prior):
                       prior=distance
            if prior is None:
                prior =0
            h=h+prior
        print("Heuristic: {}".format(h))
        return h
   
   
