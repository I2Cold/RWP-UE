import numpy as np

def argmax_v(constant_n, estimationr_and_noisez, constant_k):
    action_v = np.zeros(constant_n)
    
    ind = np.argpartition(estimationr_and_noisez, 0-constant_k)[0-constant_k:]
    for idx in ind:
        action_v[idx] = 1
        
    return action_v


def fp_produce_v(param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E):
    action_v = np.empty(constant_n)

    alpha = np.random.random()

    noise_z = np.random.exponential(param_eta, constant_n)
    if (alpha < param_gamma):
        rand_index = np.random.randint(0, constant_n)
        action_v = policyset_E[rand_index]
    else:
        action_v = argmax_v(constant_n, estimation_r + noise_z, constant_k)

    return action_v


def fp_GRAlgorithm(param_M, param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E, accumulation_z):
    result_K = np.zeros(constant_n)

    for k in range(1, (int)(param_M)):
        end = True
        simulate_v = fp_produce_v(param_gamma, constant_n, constant_k, param_eta, estimation_r, policyset_E)
        for i in range(constant_n):
            if simulate_v[i] == 1 and result_K[i] == 0:
                result_K[i] = k
            elif result_K[i] == 0:
                end = False
            
        if(end):
            break
            
    if(end == False):
        for i in range(constant_n):
            if result_K[i] == 0:
                result_K[i] = param_M

    return result_K  
