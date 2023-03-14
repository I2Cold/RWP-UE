import argparse
import time
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from method import *
from attacker import *

parser = argparse.ArgumentParser(description='Repeated Security Games')
### scenarios config
parser.add_argument('--target_num', default=150 , type=int, help='the number of targets')
parser.add_argument('--protect_num', default=15, type=int, help='the number of resources that defender will allocates')
parser.add_argument('--repeat_round', default=1500, type=int, help='the round that process will repeat')
parser.add_argument('--attacker_a', default=10, type=int, help='the ability of attacker')
parser.add_argument('--attacker_type', default='Uniform', type=str, help='attacker types: [Uniform, BestResponse, Adversarial, QuantalResponse or All]')

args = parser.parse_args()

print("==========\nArgs:{}\n==========".format(args))

constant_n = args.target_num
constant_k = args.protect_num
constant_m = args.attacker_a
constant_T = args.repeat_round

param_sigma = 2 * math.sqrt(constant_m * min(constant_m, constant_k) / constant_k)
param_gamma = math.sqrt(constant_k / constant_m / constant_T)
param_M = int(constant_n * math.sqrt(constant_m * constant_T / constant_k) * math.log(constant_T * constant_k))



utility_c = np.random.uniform(   0, 0.5, constant_n)
utility_u = np.random.uniform(-0.5,   0, constant_n)
utility = utility_c - utility_u

attacker_type = args.attacker_type

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
    
def Play(attacker_type):
    print(attacker_type)
    ### Initialize the cumulative estimated reward and random walks with 0
    estimation_r = np.zeros(constant_n)
    accumulation_z = np.zeros(constant_n)
    accumulation_r = np.zeros(constant_n)
    regret1 = np.empty(constant_T)
    regret2 = np.empty(constant_T)
    St = np.empty(constant_T)
    St[0, 0] = 0 #S1=0
    action_v_last = np.empty(constant_n)
    Dt = np.empty(constant_T)
    Dt[0, 0] = 0
    T_dx = np.array(list(range(constant_T))+1)
    
    start = time.time()
    for rdx in range(constant_T):
        action_v, accumulation_z = rw_produce_v(param_gamma, constant_n, constant_k, param_sigma, estimation_r, policyset_E, accumulation_z)
        
        action_a = attack(constant_n, constant_m, attacker_type)
        
        r = action_a * utility
        
        K = rw_GRAlgorithm(param_M, param_gamma, constant_n, constant_k, param_sigma, estimation_r, policyset_E, accumulation_z, action_v)
        regret_2 = action_v * r
        estimation_r += K * regret_2
        
        accumulation_r += r
        regret1[rdx] = argmax_v(accumulation_r, constant_k)
        regret2[rdx] = regret_2
        if rdx:
            regret2[rdx] += regret2[rdx - 1]
            if (action_v_last != action_v).any():
                St[rdx] = St[rdx - 1] + 1
            else:
                St[rdx] = St[rdx - 1]
            Dt[rdx] = Dt[rdx - 1] + np.count_nonzero(action_v_last - action_v) / 2
            
        action_v_last = action_v
        
    print('Running Time:\t {:.3f}'.format(time.time() - start))
    Rt = regret1 - regret2
    Rt = Rt / T_dx
    
    plt.subplot(3, 1 ,1)
    plt.plot(T_dx, Rt, color='b', label='RWP-UE')
    plt.xlabel('Round(t)')
    plt.xticks(T_dx, rotation='vertical')
    plt.ylabel('Average Regret')
    plt.title('Against',attacker_type ,'Attacker')
    plt.subplot(3, 1 ,2)
    plt.plot(T_dx, St, color='b', label='RWP-UE')
    plt.xlabel('Round(t)')
    plt.xticks(T_dx, rotation='vertical')
    plt.ylabel('Reallocation Times')
    plt.title('Against',attacker_type ,'Attacker')
    plt.subplot(3, 1 ,3)
    plt.plot(T_dx, Dt, color='b', label='RWP-UE')
    plt.xlabel('Round(t)')
    plt.xticks(T_dx, rotation='vertical')
    plt.ylabel('Reallocation Quantity')
    plt.title('Against',attacker_type ,'Attacker')
    plt.tight_layout()
    plt.savefig('a.png')
    plt.show()

### Play repeated security games
if attacker_type != 'All':
    Play(attacker_type)
else: #'All'
    Play('Uniform')
    Play('BestResponse')
    Play('Adversarial')
    Play('QuantalResponse')









