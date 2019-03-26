import random
import string
import itertools

VOWELS = ['a','e','i','o','u','y']
SSYL = list(set([ i[0] + i[1] for i in list(itertools.combinations(VOWELS, 2))]) - set(["iu", "iy", "au", "uy", "oy"]))
CONSONANTS = list(set(string.ascii_lowercase) - set(VOWELS) -  set("q"))

def gen_wrdl(length):
    word = ""
    for i in range(length):
        if i % 2:
            word += random.choice(CONSONANTS)
        else:
             if random.randint(1,3) == 1 and i != 1:
                word += random.choice(SSYL)
             else:
                word += random.choice(VOWELS)
    return word.capitalize()

def gen_wrd():
    return gen_wrdl(random.randint(4, 6))
