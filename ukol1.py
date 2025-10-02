import numpy as np
import sys

def generate_comments(file,number):
    buffer = ""
    for i in range(number):
        cmnt_id = np.random.randint(number)
        art_id = np.random.randint(number/10 + 10)
        user_id = np.random.randint(number/100 + 100)
        views = np.random.randint(number/1000 + 1000)
        likes = np.random.randint(views/10 + 10)
        buffer += f"{'{'}comment-id: {cmnt_id} article-id: {art_id} user-id: {user_id} text: nice views: {views} likes: {likes}{'}'}\n"
        if (number % 100000)==0:
            file.write(buffer)
            buffer = ""
    file.write(buffer)
    return file

def remove_duplicates(file):
    dictionary = {}
    for line in file:
        if line[0] != "{":
            continue
        idx = line[13:].split("\n")[0]
        if idx in dictionary:
            dictionary[idx] += 1
        else:
            dictionary[idx] = 1
    dict_size = sys.getsizeof(dictionary)
    return dict_size


with open("comments.txt","w+") as file_c:
    generate_comments(file_c,1000000)
    
with open("comments.txt","r+") as file_c:
    duplicates_dict = remove_duplicates(file_c)
print(f"Soubor ma {duplicates_dict} bajtu.")
    