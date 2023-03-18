import numpy as np
import random

pre_v = 1
param_lambda = 2

def attack_produce_v(constant_n, constant_m, attacker_type, rdx, action_v_last, utility_c, utility_u):
    action_a = np.zeros(constant_n)
    global pre_v
    
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
        
        Ua = (pre_v - 1) * utility_u
        ind = np.argpartition(Ua, 0-constant_m)[0-constant_m:]
        for idx in ind:
            action_a[idx] = 1
        
    elif attacker_type == 'Adversarial':
        if rdx > 1:
            pre_v = pre_v + (action_v_last - pre_v) / rdx
        elif rdx: #rdx==1
            pre_v = action_v_last
        else: #rdx==0
            pre_v = np.ones(constant_n) / constant_n
           
        Ud = (pre_v - 1) * utility_u - pre_v * utility_c
        ind = np.argpartition(Ud, 0-constant_m)[0-constant_m:]
        for idx in ind:
            action_a[idx] = 1
            
    else: #QuantalResponse
        #BRQR, not SU-BRQR
        if rdx > 1:
            pre_v = pre_v + (action_v_last - pre_v) / rdx
        elif rdx: #rdx==1
            pre_v = action_v_last
        else: #rdx==0
            pre_v = np.ones(constant_n) / constant_n
        
        # Ud = pre_v * utility_c
        Ua = (pre_v - 1) * utility_u
        exp_Ua = np.exp(Ua * param_lambda)
        q = exp_Ua / np.sum(exp_Ua)
        accu_q = np.empty(constant_n)
        accu_q[0] = q[0]       
        for idx in range(1, constant_n):
            accu_q[idx] = accu_q[idx - 1] + q[idx]
        k = 0
        while( k < constant_m):
            a = np.random.random()
            for idx in range(constant_n):
                if a <= accu_q[idx]:
                    if action_a[idx] == 0:
                        action_a[idx] = 1
                        k += 1
                    break
        
    return action_a