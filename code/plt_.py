import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt_num = 1
import os.path as osp

def Plt(T_dx, Rt_rw, St_rw, Dt_rw, Rt_fp, St_fp, Dt_fp, Rt_fpl, St_fpl, Dt_fpl, attacker_type, save_path):
    global plt_num
    print("start plt")
    plt.figure(plt_num)
    plt_num += 1
    plt.plot(T_dx, Rt_rw, color='b', label = 'RWP-UE')
    plt.plot(T_dx, Rt_fp, color='g', label = 'FPL-UE')
    plt.plot(T_dx, Rt_fpl, color='y', label = 'FPL')
    plt.xlabel('Round(t)')
    plt.ylabel('Average Regret')
    plt.title('Against '+ attacker_type +' Attacker')
    plt.legend()
    plt.savefig(osp.join(save_path, 'Average Regret ' + attacker_type + '.png'))
    
    plt.figure(plt_num)
    plt_num += 1
    plt.plot(T_dx, St_rw, color='b', label = 'RWP-UE')
    plt.plot(T_dx, St_fp, color='g', label = 'FPL-UE')
    plt.plot(T_dx, St_fpl, color='y', label = 'FPL')
    plt.xlabel('Round(t)')
    plt.ylabel('Reallocation Times')
    plt.title('Against '+ attacker_type +' Attacker')
    plt.legend()
    plt.savefig(osp.join(save_path, 'Reallocation Times ' + attacker_type + '.png'))
    
    plt.figure(plt_num)
    plt_num += 1
    plt.plot(T_dx, Dt_rw, color='b', label = 'RWP-UE')
    plt.plot(T_dx, Dt_fp, color='g', label = 'FPL-UE')
    plt.plot(T_dx, Dt_fpl, color='y', label = 'FPL')
    plt.xlabel('Round(t)')
    plt.ylabel('Reallocation Quantity')
    plt.title('Against '+ attacker_type +' Attacker')
    plt.legend()
    plt.savefig(osp.join(save_path, 'Reallocation Quantity ' + attacker_type + '.png'))
    #plt.tight_layout()
    #plt.show()
