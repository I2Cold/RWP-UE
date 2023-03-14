import numpy as np

def attack(constant_n, constant_m, attacker_type):
    action_a = np.zeros(constant_n)
	if attacker_type == 'Uniform':
        idx_list = list(range(constant_n))
        random.shuffle(idx_list)
        idx_list = idx_list[:constant_k]
        for gendx in idx_list:
            action_a[gendx] = 1
        
    elif attacker_type == 'BestResponse':
        1
    elif attacker_type == 'Adversarial':
        1
    else: #QuantalResponse
        1
        
    return action_a