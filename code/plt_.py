import matplotlib.pyplot as plt

plt_num = 1
def Plt(T_dx, Rt, St, Dt, attacker_type, method):
    plt.figure(plt_num)
    plt_num += 1
    plt.plot(T_dx, Rt, color='b', label = method)
    plt.xlabel('Round(t)')
    plt.ylabel('Average Regret')
    plt.title('Against '+ attacker_type +'Attacker')
    plt.savefig('Average Regret ' + attacker_type+'-'+method+'.png')
    
    plt.figure(plt_num)
    plt_num += 1
    plt.plot(T_dx, St, color='b', label = method)
    plt.xlabel('Round(t)')
    plt.ylabel('Reallocation Times')
    plt.title('Against '+ attacker_type +'Attacker')
    plt.savefig('Reallocation Times ' + attacker_type+'-'+method+'.png')
    
    plt.figure(plt_num)
    plt_num += 1
    plt.plot(T_dx, Dt, color='b', label = method)
    plt.xlabel('Round(t)')
    plt.ylabel('Reallocation Quantity')
    plt.title('Against '+ attacker_type +'Attacker')
    plt.savefig('Reallocation Quantity ' + attacker_type+'-'+method+'.png')
    #plt.tight_layout()
    #plt.show()