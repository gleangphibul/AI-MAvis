# Import necessary modules from your files
import os
import subprocess
import numpy as np

from tqdm.notebook import tqdm

from searchclient.agent_types.classic import * 

# Import all action classes (used for hardcoding solutions) and actions libraries
from searchclient.domains.hospital.actions import (
    NoOpAction, MoveAction, PushAction, PullAction, AnyAction, DEFAULT_MAPF_ACTION_LIBRARY, DEFAULT_HOSPITAL_ACTION_LIBRARY
)

# Import state, goal description and level classes for the MAvis hospital environment
from searchclient.domains.hospital.state import HospitalState
from searchclient.domains.hospital.goal_description import HospitalGoalDescription
from searchclient.domains.hospital.level import HospitalLevel

# Import the Graph-Search algorithm
from searchclient.search_algorithms.graph_search import graph_search

# Import the different search strategies for both uninformed and informed search
from searchclient.strategies.bfs import FrontierBFS
from searchclient.strategies.dfs import FrontierDFS
from searchclient.strategies.bestfirst import FrontierBestFirst, FrontierGreedy, FrontierAStar

# Import heuristic classes, to be used in informed search methods
from searchclient.domains.hospital.heuristics import (
    HospitalZeroHeuristic, HospitalGoalCountHeuristics, HospitalAdvancedHeuristics
)

# Ensure the environment is set up properly
import sys
path1= sys.argv[2]
path='levels/'+path1+'.lvl'
# Function to load a level file
def load_level_file_from_path(path):
    with open(path, "r") as f:
        lines = f.readlines()
        lines = list(map(lambda line: line.strip(), lines))
        return lines
  
# Example usage: load_level('path_to_level_file.lvl')
level_path = path
level_lines = load_level_file_from_path(level_path)
level = HospitalLevel.parse_level_lines(level_lines)

# We can access the initial state of the level using the following code
initial_state = HospitalState(level, level.initial_agent_positions, level.initial_box_positions)

# We can access the goal description of the level using the following code
goal_description = HospitalGoalDescription(level, level.box_goals + level.agent_goals)



from PIL import Image
from renderState import *

# Render some state of the level (here the initial state)
render_state(level_path=level_path, state=initial_state, output_path='Images/'+path1)

# So the state looks like this in .txt format (what the computer uses):

# And the initial state looks like this in .png:
# You can either show the image in the notebook or open it in a new window
img = Image.open('Images/'+path1+'.png')


def render_plan(level_path, plan, strategy_name, heuristic_name, num_generated, elapsed_time, sol_length):

    str_plan = convert_plan_to_string(plan) #convert the plan to a string

    # this just makes sure that the meta information is displayed correctly in the visualization
    if strategy_name == 'greedy' or strategy_name == 'astar':
        strategy_name_pygame = strategy_name + ' w. ' + heuristic_name
    else:
        strategy_name_pygame = strategy_name
    
    subprocess.run(["python3", 
                    "renderMAvis.py", 
                    "--level", level_path, 
                    "--plan", str_plan, 
                    "--search_strategy", strategy_name_pygame, 
                    "--num_generated", str(num_generated), 
                    "--time_elapsed", str(elapsed_time), 
                    "--sol_length", str(sol_length)])



# For easiness of use, let's redifine and reload everything  
level_path = path
level_lines = load_level_file_from_path(level_path)
level = HospitalLevel.parse_level_lines(level_lines)

# We can access the initial state of the level using the following code
initial_state = HospitalState(level, level.initial_agent_positions, level.initial_box_positions)

# We can access the goal description of the level using the following code
goal_description = HospitalGoalDescription(level, level.box_goals + level.agent_goals)


action_library = DEFAULT_MAPF_ACTION_LIBRARY

action_set = [action_library] * level.num_agents


heuristic_name = "zero" 
heuristic = {
        'zero': HospitalZeroHeuristic,
        'goalcount': HospitalGoalCountHeuristics,
        'advanced': HospitalAdvancedHeuristics,
    }.get(heuristic_name, HospitalZeroHeuristic)() # make sure you understand what .get() does

print('\n')
# print('BFS START')
# # Finally, let's pick the search strategy and fetch the relevant frontier
# strategy_name = "bfs" 
# frontier = {
#         'bfs': FrontierBFS,
#         'dfs': FrontierDFS,
#         'astar': lambda: FrontierAStar(heuristic),
#         'greedy': lambda: FrontierGreedy(heuristic)
#     }.get(strategy_name, FrontierBFS)() # make sure you understand what .get() does

# n_trials = 10

# plans, sol_lengths, generated, elapsed = [], [], [], []
# for n in tqdm(range(n_trials)):
#     planning_success, plan, num_generated, elapsed_time = graph_search(initial_state, action_set, goal_description, frontier)
#     plans.append(plan)
#     sol_lengths.append(len(plan))
#     generated.append(int(num_generated))
#     elapsed.append(elapsed_time)


# # The graph search function returns the following:
# print('Average solution legth:', np.mean(sol_lengths))
# print('Solution length variance :', np.var(sol_lengths))
# print('Average number of states generated:', np.mean(generated))
# print('Number of states generated variance :', np.var(generated))

print('\n')
print('DFS START')
strategy_name = "bfs" 
frontier = {
        'bfs': FrontierBFS,
        'dfs': FrontierDFS,
        'astar': lambda: FrontierAStar(heuristic),
        'greedy': lambda: FrontierGreedy(heuristic)
    }.get(strategy_name, FrontierBFS)() # make sure you understand what .get() does

n_trials = 1

plans, sol_lengths, generated, elapsed = [], [], [], []
for n in tqdm(range(n_trials)):
    planning_success, plan, num_generated, elapsed_time = graph_search(initial_state, action_set, goal_description, frontier)
    plans.append(plan)
    sol_lengths.append(len(plan))
    generated.append(int(num_generated))
    elapsed.append(elapsed_time)


# The graph search function returns the following:
print('Average solution legth:', np.mean(sol_lengths))
print('Solution length variance :', np.var(sol_lengths))
print('Average number of states generated:', np.mean(generated))
print('Number of states generated variance :', np.var(generated))


