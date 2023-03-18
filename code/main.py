import argparse
import time
import numpy as np
import random
import math
from method.RandomWalkAlgorithm import *
from method.FPL_UE import *
from attack import *
from plt_ import *
import os

'''
echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc
export DISPLAY=:0.0
'''

parser = argparse.ArgumentParser(description='Repeated Security Games')
### scenarios config
parser.add_argument('--target_num', default=150 , type=int, help='the number of targets')
parser.add_argument('--protect_num', default=15, type=int, help='the number of resources that defender will allocates')
parser.add_argument('--repeat_round', default=1500, type=int, help='the round that process will repeat')
parser.add_argument('--attacker_a', default=10, type=int, help='the ability of attacker')
parser.add_argument('--attacker_type', default='All', type=str, help='attacker types: [Uniform, BestResponse, Adversarial, QuantalResponse or All]')
parser.add_argument('--save_path', default='result', type=str, help='result save path')

args = parser.parse_args()

save_path = args.save_path
if not os.path.isdir(save_path):
    os.makedirs(save_path)

print("==========\nArgs:{}\n==========".format(args))

constant_n = args.target_num
constant_k = args.protect_num
constant_m = args.attacker_a
constant_T = args.repeat_round
attacker_type = args.attacker_type

param_sigma = 2 * math.sqrt(constant_m * min(constant_m, constant_k) / constant_k)
param_eta = math.sqrt(constant_k * (math.log(constant_n)+1) / constant_m /constant_T / min(constant_m, constant_k))
param_gamma = math.sqrt(constant_k / constant_m / constant_T)
param_M = int(constant_n * math.sqrt(constant_m * constant_T / constant_k) * math.log(constant_T * constant_k))

print("sigma:", param_sigma, " eta:", param_eta, " gamma:", param_gamma, " M:", param_M)

utility_c = np.random.uniform(   0, 0.5, constant_n)
utility_u = np.random.uniform(-0.5,   0, constant_n)
utility = utility_c - utility_u

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

def FPLUE_Algorithm(attacker_type, T_dx):
    print('FPLUE - ', attacker_type)
    ### Initialize the cumulative estimated reward and random walks with 0
    estimation_r = np.zeros(constant_n)
    accumulation_r = np.zeros(constant_n)
    regret1 = np.empty(constant_T)
    regret2 = np.empty(constant_T)
    St = np.empty(constant_T)
    St[0] = 0 #S1=0
    action_v_last = np.empty(constant_n)
    Dt = np.empty(constant_T)
    Dt[0] = 0
    
    start = time.time()
    for rdx in range(constant_T):
        action_v = fp_produce_v(param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E)
        
        action_a = attack_produce_v(constant_n, constant_m, attacker_type, rdx, action_v_last, utility_c, utility_u)
        
        r = action_a * utility
        
        K = fplue_GRAlgorithm(param_M, param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E, action_v)
        regret_2 = action_v * r
        estimation_r += K * regret_2
        
        accumulation_r += r
        regret1[rdx] = np.sum(argmax_v(constant_n, accumulation_r, constant_k) * accumulation_r)
        regret2[rdx] = (1 - param_gamma) * np.sum(regret_2) + param_gamma * np.sum(np.sum(r * policyset_E)) / constant_n
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
    
    return Rt, St, Dt

def RWPUE_Algorithm(attacker_type, T_dx):
    print('RWP - ', attacker_type)
    ### Initialize the cumulative estimated reward and random walks with 0
    estimation_r = np.zeros(constant_n)
    accumulation_z = np.zeros(constant_n)
    accumulation_r = np.zeros(constant_n)
    regret1 = np.empty(constant_T)
    regret2 = np.empty(constant_T)
    St = np.empty(constant_T)
    St[0] = 0 #S1=0
    action_v_last = np.empty(constant_n)
    Dt = np.empty(constant_T)
    Dt[0] = 0
    
    start = time.time()
    for rdx in range(constant_T):
        action_v, accumulation_z = rw_produce_v(param_gamma, constant_n, constant_k, param_sigma, estimation_r, policyset_E, accumulation_z)
        
        action_a = attack_produce_v(constant_n, constant_m, attacker_type, rdx, action_v_last, utility_c, utility_u)
        
        r = action_a * utility
        
        K = rw_GRAlgorithm(param_M, param_gamma, constant_n, constant_k, param_sigma, estimation_r, policyset_E, accumulation_z, action_v)
        regret_2 = action_v * r
        estimation_r += K * regret_2
        
        accumulation_r += r
        regret1[rdx] = np.sum(argmax_v(constant_n, accumulation_r, constant_k) * accumulation_r)
        regret2[rdx] = (1 - param_gamma) * np.sum(regret_2) + param_gamma * np.sum(np.sum(r * policyset_E)) / constant_n
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
    
    return Rt, St, Dt
    
def Play(attacker_type, save_path):
    T_dx = np.array(list(range(constant_T))) + 1
    Rt_rw, St_rw, Dt_rw = RWPUE_Algorithm(attacker_type, T_dx)
    Rt_fp, St_fp, Dt_fp = FPLUE_Algorithm(attacker_type, T_dx)
    Plt(T_dx, Rt_rw, St_rw, Dt_rw, Rt_fp, St_fp, Dt_fp, attacker_type, save_path)

list_attacker_type = ['Uniform', 'BestResponse', 'Adversarial', 'QuantalResponse']
#list_attacker_type = ['Uniform', 'BestResponse', 'Adversarial']
    
### Play repeated security games
if attacker_type != 'All':
    Play(attacker_type, save_path)
else: #'All'
    for a_type in list_attacker_type:
        Play(a_type, save_path)

