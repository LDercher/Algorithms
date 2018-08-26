def sum(ll, n):
    sum = 0
    for i in range (ll,n + 1):
        sum = sum + i
    return sum

def sum_squared(ll, n):
    sum_squared = 0
    for i in range (ll,n + 1):
        sum_squared += (i*i)
    return sum_squared

def sum_const(ll, n, const):
    const_sum = 0
    for i in range (ll, n +1):
        const_sum += const
    return const_sum

def S(N):
    A = []
    for n in range (2,N+1):
        do_add_n = True
        for a in A:
            if n % a == 0:
                do_add_n = False
                break
        if do_add_n:
            A.append(n)
    return A


def main():
    print ("sum from 1 to 100 = %s \n\n" % sum(0,100))
    print ("sum squared from 1 to 100 = %s \n\n" % sum_squared(0,100))
    print ("sum of k squared plus k plus 1 from 12 to 123 = %s \n\n" % (sum_squared(12,123) + sum(12,123) + sum_const(12,123,1)))
    print ('S(10) =')
    print (S(10))
    print ('\n\nS(100) =')
    print (S(100))


main()