#!/usr/bin/env python3

from typing import List, Tuple
import numpy as np
from scipy.optimize import linear_sum_assignment

from .agent import Agent



def min_cost4(starts: List[Tuple[int, int]], goals: List[Tuple[int, int]]):
    print("start positions:")
    print(starts)
    print("end positions")
    print(goals)

    agents = []
    for i, start in enumerate(starts):
        agents.append(Agent(start, goals[i]))
    return agents

