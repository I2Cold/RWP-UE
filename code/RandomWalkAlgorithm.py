import numpy as np
from common import *
import math
from scipy.stats import truncnorm


def rw_produce_v(param_gamma, constant_n, constant_k, constant_m, estimation_r, policyset_E, accumulation_z):
    action_v = np.empty(constant_n)

    rand = np.random.random()

    sigma = 2 * math.sqrt(constant_m * constant_m / constant_k)
    noise_z = np.random.normal(0, sigma, constant_n) + accumulation_z
    if (rand < param_gamma):
        rand_index = np.random.randint(0, constant_n)
        action_v = policyset_E[rand_index]
    else:
        action_v = argmax_v(estimation_r+noise_z, constant_k)

    return action_v, noise_z


def rw_GRAlgorithm(param_M, param_gamma, constant_n, constant_k, constant_m, estimation_r, policyset_E, accumulation_z, defender_action):
    result_K = np.zeros(len(estimation_r))

    for k in range(1, (int)(param_M)+1):
        end = True
        simulate_v, _ = rw_produce_v(param_gamma, constant_n, constant_k, constant_m, estimation_r, policyset_E, accumulation_z)
        for i in range(constant_n):
            if k < param_M and simulate_v[i] == 1 and result_K[i] == 0:
                result_K[i] = k
            elif k == param_M and result_K[i] == 0:
                result_K[i] = param_M

        for i in range(constant_n):
            if result_K[i] == 0 and defender_action[i] == 1:
                end = False

        if(end):
            break

    return result_K

