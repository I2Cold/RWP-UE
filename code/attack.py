import numpy as np
import random

pre_v = 1

def attack_produce_v(constant_n, constant_m, attacker_type, rdx, action_v_last, utility_c, utility_u):
    action_a = np.zeros(constant_n)
    
	if attacker_type == 'Uniform':
        idx_list = list(range(constant_n))
        random.shuffle(idx_list)
        idx_list = idx_list[:constant_m]
        for gendx in idx_list:
            action_a[gendx] = 1
        
    elif attacker_type == 'BestResponse':
        if rdx > 1:
            pre_v = pre_v + (action_v_last - pre_v) / rdx
        elif rdx: #rdx==1
            pre_v = action_v_last
        else: #rdx==0
            pre_v = np.ones(constant_n) / constant_n
        
        pre_v_i = pre_v - np.ones(constant_n)
        pre_au = pre_v_i * utility_u
        ind = np.argpartition(pre_au, 0-constant_k)[0-constant_k:]
        for idx in ind:
            action_a[idx] = 1
        
    elif attacker_type == 'Adversarial':
        if rdx > 1:
            pre_v = pre_v + (action_v_last - pre_v) / rdx
        elif rdx: #rdx==1
            pre_v = action_v_last
        else: #rdx==0
            pre_v = np.ones(constant_n) / constant_n
           
        pre_v_i = pre_v - np.ones(constant_n)
        pre_du = pre_v_i * utility_c
        ind = np.argpartition(pre_du, 0-constant_k)[0-constant_k:]
        for idx in ind:
            action_a[idx] = 1
            
    else: #QuantalResponse
        1
        
    return action_a