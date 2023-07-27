import deepl
from credentials import *
#!/usr/bin/env python3

#Convert latex file in full file including the inputs

import argparse
import re
import sys
import os
import yaml
from constants import *    # Definition of the tag symbol and special commands/environnments
from constants_perso import *  # Personnal customization

#--------------------------------------------------
#--------------------------------------------------

# Arguments 
parser = argparse.ArgumentParser(description='Conversion a LaTex file to a text file keeping appart commands and maths.')
parser.add_argument('inputfile', help='input LaTeX filename')
parser.add_argument('outputfile', nargs='?', help='output text filename')
options = parser.parse_args()

to_translate_file = options.inputfile
translated_file = options.outputfile

input_dir=''
input_dir=''
for i in range (0,len(to_translate_file.split('\\'))-1):
    input_dir+=to_translate_file.split('\\')[i]+'\\'
print(input_dir)
# Get argument: a tex file
print(to_translate_file)

# Output file name 
if translated_file:
    txt_file = translated_file    # Name given by user
else:
    txt_file = ".."+to_translate_file.strip('.txt')+'_translated.txt' # If no name add a .txt extension

print(txt_file)
# Read file object to string



translator = deepl.Translator(auth_key)
translator.translate_document_from_filepath(to_translate_file,txt_file, target_lang="EN-GB")


