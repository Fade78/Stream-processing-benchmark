#!/usr/bin/python3

number_of_lines=1000000
seed=1337 # What else? :)

import random

def random_name(minlength=3,maxlength=7):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz')
            for x in range(random.randrange(minlength,maxlength)))

def random_float_or_int_number():
    return random.choice((
                    random.randint(1,100000),
                    random.random()*100000
                    ))
def random_line():
    field1 = random_name(4,7)
    field2 = random_name(6,10)
    field3 = random_float_or_int_number()
    return [ field1, field2, field3 ]

random.seed(seed) 

for i in range(number_of_lines):
    if random.random() < 0.01:
        # Special line!
        if random.random() < 0.1:
            # Malformed: last field is not a number
            line=random_line()
            line[-1]=random_name()
            print(i,*line,sep='\t')
        else:
            # Commentary line
            print("# this is a commentary that should be filtered out")
    else:
        print(i,*random_line(),sep='\t')
