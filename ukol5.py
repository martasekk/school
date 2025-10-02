import numpy as np
import mmh3
import math


class Hyperloglog:
    def __init__(self):
        self.b = 14
        self.m = 2 ** self.b
        self.S = np.zeros(self.m, dtype=np.int8)
        self.E = 0
        
        self.alpha16 = 0.673 
        self.alpha32 = 0.697
        self.alpha64 = 0.709
        self.alpha_m = 0.7213/(1 + 1.079/self.m) # for m >= 128

    def first_bits(self, number, n):
        num_bits = number.bit_length() 
        if n >= num_bits:
            return number 
        shift_amount = num_bits - n
        mask = ((1 << n) - 1) << shift_amount
        return (number & mask) >> shift_amount
    
    def aggregate(self, HLL2):
        for i in range(self.m):
            self.S[i] = max(self.S[i], HLL2.S[i])
        return self
    
    def calculate(self):
        V = 0
        sum_val = 0.0
        for item in self.S:
            sum_val += 1 / 2**item
            if item == 0:
                V += 1
        
        harmonic_avg = self.m / sum_val
        E = self.alpha_m * self.m * harmonic_avg
        
        if E <= 5*self.m/2:
            print("linear counting")
            if V != 0:
                E_final = self.m*np.log(self.m/V)
            else:
                E_final = E
        elif E <= 2**32 / 30:
            E_final = E
        elif E > 2**32 / 30:
            E_final = -2**32 * np.log(1 - E/2**32)
        self.E = E_final
        return E_final

    def add_and_calculate(self, M):
        for a in M:
            h1 = mmh3.hash(a)
            p = (h1 & -h1).bit_length() 
            bucket = self.first_bits(h1, self.b)
            self.S[bucket] = max(self.S[bucket], p)
        self.calculate()
        return self.E

A = np.random.randint(0,2**20,10**6)
B = np.random.randint(0,2**20,10**6)
C = np.random.randint(0,2**20,10**6)
D = np.random.randint(0,2**20,10**6)
E = np.random.randint(0,2**20,10**6)

HLL1 = Hyperloglog()
print(f"HyperLogLog 1: {HLL1.add_and_calculate(A)}")
HLL2 = Hyperloglog()
print(f"HyperLogLog 2: {HLL2.add_and_calculate(B)}")
HLL3 = Hyperloglog()
print(f"HyperLogLog 3: {HLL3.add_and_calculate(C)}")
HLL4 = Hyperloglog()
print(f"HyperLogLog 4: {HLL4.add_and_calculate(D)}")
HLL5 = Hyperloglog()
print(f"HyperLogLog 5: {HLL5.add_and_calculate(E)}")

##
#  zabiraji 5 * 2^14 bajtu
#

Abc = set(A)
print(f"HyperLogLog 1 chyba: {1 - HLL1.E/len(Abc)} ocekavana chyba: {1.04/math.sqrt(2**14)}")
Abc = set(B)
print(f"HyperLogLog 2 chyba: {1 - HLL2.E/len(Abc)} ocekavana chyba: {1.04/math.sqrt(2**14)}")
Abc = set(C)
print(f"HyperLogLog 3 chyba: {1 - HLL3.E/len(Abc)} ocekavana chyba: {1.04/math.sqrt(2**14)}")
Abc = set(D)
print(f"HyperLogLog 4 chyba: {1 - HLL4.E/len(Abc)} ocekavana chyba: {1.04/math.sqrt(2**14)}")
Abc = set(E)
print(f"HyperLogLog 5 chyba: {1 - HLL5.E/len(Abc)} ocekavana chyba: {1.04/math.sqrt(2**14)}")

print("Agregace HyperLogLogu 1 az 5")
HLL1.aggregate(HLL2).aggregate(HLL3).aggregate(HLL4).aggregate(HLL5)
HLL1.calculate()
print("Spojeni vsech 5 mnozin")
X = np.concatenate((A,B,C,D,E))
Abc = set(X)
print(f"Agregace vsech HyperLogLogu chyba: {1 - HLL1.E/len(Abc)} ocekavana chyba: {1.04/math.sqrt(2**14)}")

