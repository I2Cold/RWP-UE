import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt_num = 1

def Plt(T_dx, Rt_rw, St_rw, Dt_rw, Rt_fp, St_fp, Dt_fp, attacker_type):
    global plt_num
    plt.figure(plt_num)
    plt_num += 1
    plt.plot(T_dx, Rt_rw, color='b', label = 'RWP-UE')
    plt.plot(T_dx, Rt_fp, color='g', label = 'FPL-UE')
    plt.xlabel('Round(t)')
    plt.ylabel('Average Regret')
    plt.title('Against '+ attacker_type +' Attacker')
    plt.savefig('Average Regret ' + attacker_type + '.png')
    
    plt.figure(plt_num)
    plt_num += 1
    plt.plot(T_dx, St_rw, color='b', label = 'RWP-UE')
    plt.plot(T_dx, St_fp, color='g', label = 'FPL-UE')
    plt.xlabel('Round(t)')
    plt.ylabel('Reallocation Times')
    plt.title('Against '+ attacker_type +' Attacker')
    plt.savefig('Reallocation Times ' + attacker_type + '.png')
    
    plt.figure(plt_num)
    plt_num += 1
    plt.plot(T_dx, Dt_rw, color='b', label = 'RWP-UE')
    plt.plot(T_dx, Dt_fp, color='g', label = 'FPL-UE')
    plt.xlabel('Round(t)')
    plt.ylabel('Reallocation Quantity')
    plt.title('Against '+ attacker_type +' Attacker')
    plt.savefig('Reallocation Quantity ' + attacker_type + '.png')
    #plt.tight_layout()
    #plt.show()
