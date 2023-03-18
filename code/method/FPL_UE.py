import numpy as np

def argmin_v(constant_n, estimationr_and_noisez, policyset_E):
    
    max_value = -100
    idx = 0
    for i in range(constant_n):
        value = np.sum(policyset_E[i] * estimationr_and_noisez)
        if max_value < value:
            max_value = value
            idx = i
        
    return policyset_E[idx]

def fpl_produce_v(param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E):
    action_v = np.empty(constant_n)

    z = np.random.exponential(param_eta, constant_n)
    action_v = argmin_v(constant_n, estimation_r + z, policyset_E)

    return action_v

def fpl_GRAlgorithm(param_M, param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E, defender_action):
    result_K = np.zeros(constant_n)
    end = True
    for k in range(1, (int)(param_M)):
        end = True
        simulate_v = fpl_produce_v(param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E)
        for i in range(constant_n):
            if simulate_v[i] == 1 and result_K[i] == 0:
                result_K[i] = k
            elif result_K[i] == 0 and defender_action[i]==1:
            # improved FPL-UE, running faster
                end = False
            
        if(end):
            break
            
    if(end == False):
        for i in range(constant_n):
            if result_K[i] == 0:
                result_K[i] = param_M

    return result_K

def argmax_v(constant_n, estimationr_and_noisez, constant_k):
    action_v = np.zeros(constant_n)
    
    ind = np.argpartition(estimationr_and_noisez, 0-constant_k)[0-constant_k:]
    for idx in ind:
        action_v[idx] = 1
        
    return action_v

def fp_produce_v(param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E):
    action_v = np.empty(constant_n)

    alpha = np.random.random()
    if (alpha < param_gamma):
        rand_index = np.random.randint(0, constant_n)
        action_v = policyset_E[rand_index]
    else:
        z = np.random.exponential(param_eta, constant_n)
        action_v = argmax_v(constant_n, estimation_r + z, constant_k)

    return action_v

def fplue_GRAlgorithm(param_M, param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E, defender_action):
    result_K = np.zeros(constant_n)
    end = True
    for k in range(1, (int)(param_M)):
        end = True
        simulate_v = fp_produce_v(param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E)
        for i in range(constant_n):
            if simulate_v[i] == 1 and result_K[i] == 0:
                result_K[i] = k
            elif result_K[i] == 0 and defender_action[i]==1:
            # improved FPL-UE, running faster
                end = False
            
        if(end):
            break
            
    if(end == False):
        for i in range(constant_n):
            if result_K[i] == 0:
                result_K[i] = param_M

    return result_K