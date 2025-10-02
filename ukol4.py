import bf
import numpy as np
import time as t

max = 10**7
U = np.random.randint(0,max,10**6)

bfl = bf.BloomFilter(10**6, 0.0214)
print(">Inserting data into BF")
for j in U:
   bfl.insert(str(j))
print(">Complete")

found = 0
falsepositive = 0
elapsed_time = 0

for i in range(10000):
    number = str(np.random.randint(max))
    
    t0 = t.time()
    bf_found = bfl.lookup(number)
    t1 = t.time()
    
    if bf_found:
        found += 1
        if (len(np.where(U==np.int64(number))[0])==0):
            falsepositive += 1
    elapsed_time += t1 - t0
    
print("Hledani trvalo: ",elapsed_time)
print("Nalezeno: ", found - falsepositive, "prvku")
print("Chybovost: ",100*falsepositive/10000,"%")

###############################################################################
max = 10**5
U = np.random.randint(0,max,10**4)

bfl1 = bf.BloomFilter(10**4, 0.0214)
print(">Inserting data into BF1")
for j in U:
   bfl1.insert(str(j))
print(">Complete")



found = 0
falsepositive = 0
elapsed_time = 0

for i in range(10000):
    number = str(np.random.randint(max))
    
    t0 = t.time()
    bf_found = bfl1.lookup(number)
    t1 = t.time()
    
    if bf_found:
        found += 1
        if (len(np.where(U==np.int64(number))[0])==0):
            falsepositive += 1
    elapsed_time += t1 - t0
    
print("Hledani trvalo: ",elapsed_time)
print("Nalezeno: ", found - falsepositive, "prvku")
print("Chybovost: ",100*falsepositive/10000,"%")

###############################################################################
max = 10**9
U = np.random.randint(0,max,10**8)

bfl2 = bf.BloomFilter(10**8, 0.0214)
print(">Inserting data into BF2")
for j in U:
   bfl2.insert(str(j))
print(">Complete")

found = 0
falsepositive = 0
elapsed_time = 0

for i in range(10000):
    number = str(np.random.randint(max))
    
    t0 = t.time()
    bf_found = bfl2.lookup(number)
    t1 = t.time()
    
    if bf_found:
        found += 1
        if (len(np.where(U==np.int64(number))[0])==0):
            falsepositive += 1
    elapsed_time += t1 - t0
    
print("Hledani trvalo: ",elapsed_time)
print("Nalezeno: ", found - falsepositive, "prvku")
print("Chybovost: ",100*falsepositive/10000,"%")

##
#  Doba hledani se zvetsila s velikosti dat
#  Pokud bych nezvetsil pocet prvku n v bloom filteru,
#  tak by chybovost klesla s mensim poctem prvku a s
#  vetsim poctem by se zvysila