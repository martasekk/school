import numpy as np
import time as time

file_name = "Array.txt"

def generate_numbers_into_file(amount):
    arr = np.zeros(amount)
    arr[0] = np.random.randint(20)
    for i in range(amount - 1):
        arr[i+1] = arr[i] + np.random.randint(19) + 1
    with open(file_name, "w+") as file:
        np.savetxt(file, arr, fmt="%i", newline=" ")
        return file.name
    
def binary_search_from_file(file, number):
    arr = []
    with open(file, "r") as f:
        arr = np.loadtxt(f, dtype=int)
    
    start_time = time.time()
    counter = 0
    idx = 0
    lower = 0
    higher = arr.size - 1
    while (lower <= higher):
        counter += 1
        idx = int(np.fix((lower + higher)/2))
        if (arr[idx] < number):
            lower = idx + 1
        elif (arr[idx] > number):
            higher = idx - 1
        else:
            break
    elapsed_time = time.time() - start_time
    if (arr[idx]==number):
        print("Prvek ", number, " byl nalezen, doba hledani: ", elapsed_time, " sekund, hledani probehlo v ", counter," krocich, pocet kroku linearniho pruchodu: ", idx)
        return idx
    else:
        print("Prvek ", number, " nebyl nalezen, doba trvani: ", elapsed_time, " sekund, hledani probehlo v ", counter," krocich, pocet kroku linearniho pruchodu: ", idx)
    
    return -1
    
#####################################################################################
#
#   Jmeno souboru je ulozeno nahore jako globalni promenna: file_name = "Array.txt"
#

amount = 800000000
file = generate_numbers_into_file(amount)

for i in range(10):
    binary_search_from_file(file_name, np.random.randint(amount*10))
