import subprocess
import shutil
import glob
import math
import os
import datetime
import time
import sys


# ----------------------------------------------------------------------------------------
# Function to extract a specific parameter from a PRISMS-CPFE input file
# ----------------------------------------------------------------------------------------
def parameter_extractor(file_name, entry_name):
    parameter_value = 0

    num_words_in_entry_name = len(entry_name.split())
    entry_name_no_whitespace = "".join(entry_name.split())

    f = open(file_name)
    for line in f:
        words_in_line = line.split()
        if len(words_in_line) > 0:
            if words_in_line[0] == "set":
                if (len(words_in_line) > num_words_in_entry_name+2):
                    prospective_match = ""
                    for word in range(1, 1+num_words_in_entry_name):
                        prospective_match += words_in_line[word]
                    if (prospective_match == entry_name_no_whitespace):
                        if len(words_in_line) >= 2+num_words_in_entry_name:
                            parameter_value = words_in_line[2+num_words_in_entry_name]

    f.close()
    return parameter_value


# ----------------------------------------------------------------------------------------
# Function to take a line of split strings and create a key-value pair from them
# ----------------------------------------------------------------------------------------
def parse_line(split_line):
    # Still need to write this
    equal_sign_index = -1
    for index, word in enumerate(split_line):
        if word == '=':
            equal_sign_index = index

    if equal_sign_index == -1:
        entry_value = "Invalid Entry"
        entry_name = " ".join(split_line[1:len(split_line)-1])
        return entry_name, entry_value

    entry_name = " ".join(split_line[1:equal_sign_index])
    entry_value = " ".join(split_line[equal_sign_index+1:len(split_line)])
    #print "ENTRY: ", entry_name, "VALUE: ", entry_value

    return entry_name, entry_value


# ----------------------------------------------------------------------------------------
# PRISMS-CPFE input file parsing script
# ----------------------------------------------------------------------------------------
# This file reads a PRISMS-CPFE input file and turns it into a set of key-value pairs that
# are stored in a dictionary
def parse_parameters_file():

    file_name = "parameters.in"

    parameter_set = {}
    in_subsection = False

    f = open(file_name)
    for line in f:

        # First make sure line isn't a comment or blank line
        stripped_line = line.strip()
        if len(stripped_line) < 1 or stripped_line[0] is "#":
            continue

        # Check if entering or leaving a subsection (not needed once updates are complete)
        split_line = stripped_line.split()
        if split_line[0] == "subsection":
            in_subsection = True
            subsection_name = ' '.join(split_line[1:-1])
            subsection_name = subsection_name[:-1]
            subsection_name = subsection_name + " (" + split_line[-1] + ")"
            # print("subsection name: " + subsection_name)

        elif split_line[0] == "end":
            in_subsection = False

        # For non-subsection variables
        if in_subsection is False and split_line[0] == "set":
            parameter_key_value_pair = parse_line(split_line)
            parameter_set[parameter_key_value_pair[0]] = parameter_key_value_pair[1]
        elif in_subsection is True and split_line[0] == "set":
            parameter_key_value_pair = parse_line(split_line)
            parameter_set[subsection_name + ": " + parameter_key_value_pair[0]] = parameter_key_value_pair[1]
            # print(subsection_name + ": " + parameter_key_value_pair[0])

    return parameter_set
