import bf
import numpy as np
import random
import time as t

file_name = "Array.txt"
bfl = bf.BloomFilter(10000000, 0.02)

low = 0
high = 1000000000000
size_u = 10000000

print(">Creating U")
U = np.random.randint(0,high,size_u,dtype=np.int64)
print(">Complete")

print(">Inserting U into BF")
for j in U:
   bfl.insert(str(j))
print(">Complete")

print(">Saving U into file")
with open(file_name,"w+") as arr_file:
   np.savetxt(arr_file,U,fmt='%s')
print(">Complete")
 
searches = 1000000

found = 0
falsepositive = 0
elapsed_time_rand = 0

print("Nahodne hledani:")
for i in range(searches):
   number = str(np.random.randint(high, dtype=np.int64))
   
   t0 = t.time()
   bf_found = bfl.lookup(number)
   t1 = t.time()
   
   if bf_found:
      found += 1
      if (len(np.where(U==np.int64(number))[0])==0):
         falsepositive += 1
   elapsed_time_rand += t1 - t0
      
print("Hledani trvalo: ",elapsed_time_rand)
print("Nalezeno: ", found - falsepositive, "prvku")
print("Chybovost: ",100*falsepositive/searches,"%")

lines = open(file_name, "r").read().splitlines()

# nahodne zamichani prvku 
random.shuffle(lines)

# omezeni na 10^6 prvku
lines = lines[:searches]

elapsed_time_success = 0

print("Uspesne hledani:")
for number in lines:
   
   t0 = t.time()
   bf_found = bfl.lookup(number)
   t1 = t.time()

   elapsed_time_success += t1 - t0
   
print("Hledani trvalo: ", elapsed_time_success)
print("Uspesne hledani vsech prvku trvalo o ", elapsed_time_success - elapsed_time_rand, "dele")
      