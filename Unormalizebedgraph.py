# Unormalizebedgraphs v1.1

import argparse
import os
from array import *

#get arguments from command line
parser = argparse.ArgumentParser(description='Uaveragebedgraphs_args')
parser.add_argument('-o','--output', help='name of output file', required=True, type=str)
parser.add_argument('-f','--file', help='file to be normalized', required=True, type=str)
parser.add_argument('-n','--norm', help='file to be normalized', required=True, type=float)
args = vars(parser.parse_args())
file = args['file']
output_file = args['output']
factor = args['norm']

def add (input, newfile):

# make list of chromosomes
    chromosomes = []
    with open(file) as f:
        for line in f:
            line_split = line.split("\t")
            if line_split[0] not in chromosomes:
                chromosomes.append(line_split[0])

    done = "no"
    while done == "no":
        try:
            current_chromosome = chromosomes.pop(0)
        except:
            break

# get length of current chromosome
        stop = 0
        with open(file) as f:
            for line in f:
                line_split = line.split("\t")
                if line_split[0] == current_chromosome:
                    if int(line_split[2]) > stop:
                        stop = int(line_split[2])
        if stop > 0:  #continue only if values in chromosome
            output = array('f', [0.0] * stop)

#normalize
        with open(file) as f:
            for line in f:
                line_split = line.split("\t")
                line_split[3] = line_split[3].replace("\n", "")
                if line_split[0] == current_chromosome:
                    if float(line_split[3]) > 0:
                        for o in range(int(line_split[2]) - int(line_split[1])):
                            coord = o + int(line_split[1])
                            output[coord] = output[coord] + float(line_split[3]) / factor



#concatenate entries with same value
            output2 = []
            temp_entry = []
            for x, value in enumerate(output):
                if value != 0:
                    if temp_entry == []:
                        temp_entry = [current_chromosome, x, x + 1, value]
                    elif temp_entry[3] == value:
                        temp_entry[2] += 1
                    elif temp_entry[3] != value:
                        output2.append(temp_entry)
                        temp_entry = [current_chromosome, x, x + 1, value]
                else: temp_entry == []

            if temp_entry != []:
                output2.append(temp_entry)

            with open(newfile, "a") as f:
                for row in output2:
                    f.write(str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2]) + "\t" + str(row[3]) + "\n")

############################################################################

add(file, output_file)
print("Success :)")
