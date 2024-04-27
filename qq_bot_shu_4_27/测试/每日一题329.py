import time
#n=int(input())
#n*=2
#m=int(n**0.5)
#print(m,"行")
for num in range(1,10000000000):
    num *= 2
    num_hang = int(num ** 0.5)
    mun=num/2
    num=num/2
    i = 0
    while mun>0:
        i+=1
        mun-=i
    if i==num_hang:
        print("成功")
        print()
    else:
        print(i,num_hang)
        print(num ** 0.5)
        print(mun,num)
    time.sleep(0.2)




