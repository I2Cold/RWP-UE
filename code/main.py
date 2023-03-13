import argparse
import time
import numpy as np
import random
from common import *
from method import *
from attacker import *

parser = argparse.ArgumentParser(description='Repeated Security Games')
### scenarios config
parser.add_argument('--target_num', default=150 , type=int, help='the number of targets')
parser.add_argument('--protect_num', default=15, type=int, help='the number of resources that defender will allocates')
parser.add_argument('--repeat_round', default=1500, type=int, help='the round that process will repeat')
parser.add_argument('--attacker_type', default='Uniform', type=str, help='attacker types: [Uniform, BestResponse, Adversarial, QuantalResponse or all]')

### hyperparameter config
parser.add_argument('--gamma', default=0.1 , type=float, help='exploration rate')
parser.add_argument('--threshold', default=10, type=int, help='the maximum number of times required for the first occurrence of event')

args = parser.parse_args()

print("==========\nArgs:{}\n==========".format(args))

constant_n = args.target_num
constant_k = args.protect_num
param_M = args.threshold
param_gamma = args.gamma

### what is constant_m? hyperparameter to control sigma?

utility_c = np.random.uniform(   0, 0.5, constant_n)
utility_u = np.random.uniform(-0.5,   0, constant_n)

attacker_type = args.attacker_type

### Initialize the cumulative estimated reward and random walks with 0
estimation_r = np.zeros(constant_n)
accumulation_z = np.zeros(constant_n)

### Pick the set of exploration strategies
policyset_E = np.zeros((constant_n, constant_n))
for idx in range(constant_n):
    idx_list = list(range(constant_n))
    idx_list.pop(idx)
    random.shuffle(idx_list)
    idx_list = idx_list[:constant_k]
    policyset_E[idx, idx] = 1
    for gendx in idx_list:
        policyset_E[idx, gendx] = 1
    
### Play repeated security games
for rdx in range(args.repeat_round):

    action_v, accumulation_z = rw_produce_v(param_gamma, constant_n, constant_k, constant_m, estimation_r, policyset_E, accumulation_z)
    
    action_a = attack(attacker_type)
    
    r = 0
    for idx in range(constant_n):
        if action_a[idx] == 1 and action_v[idx] == 1:
            r += utility_c[idx]
        elif action_a[idx] == 1:
            r += utility_u[idx]
    
    rw_GRAlgorithm(param_M, param_gamma, constant_n, constant_k, constant_m, estimation_r, policyset_E, accumulation_z, defender_action)












