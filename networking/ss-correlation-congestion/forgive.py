#!/usr/bin/env python3

"""
    forgive.py - preprocesses a file with tag-value pairs in a forgiving 
    fashion. The whole file is read into memory, processed and then stored
    to memory again, line-by-line processing is not possible.

    usage: ./forgive.py <input-file> <output-file>

    Handles different tag-value formats: tag:value, tag value
    Handles tags without value: tag
    Handles different number formats: num, num.num
    Handles optionale dimensions: numdim

    Note: ',' is understood as a seperatur between two values, not as a 
    decimal seperator.

    Originally developed to make the output of the 'ss' utility (for 
    investigating sockets) useable with gnuplot. 
    
    The output looks like this (without leading line numbers, note that empty 
    fields are possible):
    1: tag1,tag2,tag3,tag4
    2: 1,2,3,4
    3: 1,,,4

    Internally, we try to build up the table 'forgive' that looks like e.g.:
       name:       |    rtt    |  jitter  |   bw    |
                   |-----------|----------|---------|
       dimension:  |    ms     |    ms    |  Mbits  |
                   |-----------|----------|---------|
       payload 1:  |    10     |     2    |   10    |
                   |-----------|----------|---------|
       payload 2:  |    12     |     3    |   10    |
                   |-----------|----------|---------|
       payload 3:  |    13     |     1    |   10    |
                   |-----------|----------|---------|
    The first row holds all tag names, the second row all dimensions, and all
    following rows the payload data.

"""

import os
import sys
import time

forgive = []
height = 0
width = 0

def usage():
    print("usage: ./forgive.py <input-file> [<output-file>]")

if len(sys.argv) < 2 or len(sys.argv) > 3:
    usage()
    sys.exit()

input_file = sys.argv[1]
if len(sys.argv) == 3:
    output_file = sys.argv[2]
else:
    output_file = ''

if os.access(input_file, os.R_OK) == False:
    print("can't reat input file", input_file)
    sys.exit()

if os.access(input_file, os.W_OK) == False:
    print("can't write output file", output_file)
    sys.exit()

''' 
    splits the incoming line of text into tokens
    e.g. "test tokenize" becomes ["test", "tokenize"]
'''
def tokenize(line):
    tokens = [line]
    while True:
        seperator = ''
        for token in tokens:
            for ch in token:
                if not ch.isalnum() and not ch == '.' and not ch == '_':
                    seperator = ch
                    break
            if seperator != '':
                break
        if seperator != '':
            new_tokens = []
            for token in tokens:
                new_tokens = new_tokens + token.split(seperator)
            tokens = new_tokens
        else:
            break
    return tokens

''' 
    checks on a list of tokens if it is a tag or value (num)
    e.g. ["some","123"] becomes [("tag","some"),("num","123")]
'''
def tag(tokens):
    tagged = []
    for token in tokens:
        if len(token) > 0:
            ch = token[0]
            if ch.isdigit():
                tagged = tagged + [('num', token)]
            else:
                tagged = tagged + [('tag', token)]
    return tagged

'''
    splits the dimension from the value in a list of tokens
    e.g. [("num","123ms")] becomes [("num","123","ms")]
'''
def split_dimensions(tagged):
    new_tagged = []
    for t in tagged:
        kind = t[0]
        if kind == 'num':
            dimension = ''
            value = t[1]
            for c in reversed(value):
                if c.isdigit():
                    break
                else:
                    dimension = c + dimension
            if dimension != '':
                value = t[1][0:-len(dimension)]
                t = (t[0], value, dimension)
        new_tagged += [t]
    return new_tagged

''' 
    searches the first row of the global table for tag and returns its index
    if found, (False, -1) otherwise
''' 
def find_column_for_tag(tag):
    column_index = 0
    for col in forgive:
        if col[0] == tag:
            return (True, column_index)
        column_index += 1
    return (False, -1)

'''
    runs through all the numbers in a tagged list of tokens and tries to find
    the matching identifier (the last token beforehand that was a tag), stores
    its findings in the global table
'''
def assign_tag_to_number(tagged, linenum):
    global forgive
    for i in range(len(tagged)):
        elem = tagged[i]
        kind = elem[0]
        val = elem[1]
        if len(elem) == 3:
            dim = elem[2]
        else:
            dim = ''
        if kind == 'num':
            j = i
            while j > 0:
                assigned = False
                if tagged[j][0] == 'tag':
                    assigned = True
                    name = tagged[j][1]
                    match, index = find_column_for_tag(name)
                    if match:
                        forgive[index][linenum+2] = val
                        if dim != '':
                            if forgive[index][1] != '' and forgive[index][1] != dim:
                                raise Exception('Different dimensions')
                            forgive[index][1] = dim
                    else:
                        raise Exception('Should never happen')
                if assigned:
                    break
                j -= 1

'''
    takes a list of tagged tokens and enriches the result table with new names
'''
def enrich_tags(input):
    global forgive
    for t in input:
        kind = t[0]
        if kind == 'tag':
            name = t[1]
            match, index = find_column_for_tag(name)
            if not match:
                col = []
                col += [name, '']
                col += ['?'] * (height - 2)
                forgive += [col]

'''
    iterate over the file and count the total line numbers
'''
def count_total_input_lines(in_file):
    i = 0
    for line in in_file:
        i += 1
    return i

'''
    iterate over the file to find all occuring tags
'''
def find_all_tags(in_file):
    for line in in_file:
        enrich_tags(tag(tokenize(line)))
    return len(forgive)

'''
    todo
'''
def merge_dimensions_into_tag_names():
    i = 0
    while i < width:
        if forgive[i][1] != '':
            forgive[i][0] += '(' + forgive[i][1] + ')'
        del(forgive[i][1])
        i += 1

'''
    todo
'''
def delete_underscore_in_tag_names():
    i = 0
    while i < width:
        forgive[i][0] = forgive[i][0].replace('_','')
        i += 1

'''
    todo
'''
def delete_columns_without_data():
    global width
    i = 0
    while i < width:
        j = 1
        has_data = False
        while j < height-3:
            if forgive[i][j] != '?':
                has_data = True
                break
            j += 1
        if not has_data:
            del(forgive[i])
            width -= 1
        else:
            i += 1

# todo make height influencers actually incluence height!!!

def write_table_to_file(f):
    i = 0
    while i < height - 1:
        j = 0
        while j < width:
            f.write(forgive[j][i] + ',')
            j += 1
        i += 1
        f.write('\n')




'''
    iterate over the file to fill the result table (the actual work happens here)
'''
def build_table(in_file):
    i = 0
    for line in in_file:
        dimmed = split_dimensions(tag(tokenize(line)))
        assign_tag_to_number(dimmed, i)
        i += 1
    # postprocessing
    merge_dimensions_into_tag_names()
    delete_underscore_in_tag_names()
    delete_columns_without_data()

'''
    writes the global result table to file f
'''
def write_table_to_file(f):
    i = 0
    while i < height - 1:
        j = 0
        while j < width:
            f.write(forgive[j][i] + ',')
            j += 1
        i += 1
        f.write('\n')

with open(input_file) as f:
    ''' pass 1: count total lines '''
    height = count_total_input_lines(f) + 2
    f.seek(0)
    
    ''' pass 2: find all tags '''
    width = find_all_tags(f)
    f.seek(0)
    
    ''' pass 3: fill in all the data '''
    build_table(f)

    # print_table()
    if output_file != '':
        with open(output_file, 'w') as out:
            write_table_to_file(out)
    else:
        write_table_to_file(sys.stdout)
