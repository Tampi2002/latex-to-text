#!/usr/bin/env python3

# Convert a LaTeX file to txt file
# Usage : 'python3 latextotext.py toto.tex'
# Output : create a file toto.txt and a file toto.dic


# Author: Arnaud Bodin. Thanks to Kroum Tzanev
# Idea from Mr.Sh4nnon https://codereview.stackexchange.com/questions/209049
# Licence CC-BY-SA 4.0

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
parser.add_argument('dicfile', nargs='?', help='output dictionnary filename')
options = parser.parse_args()

tex_file = options.inputfile
output_file = options.outputfile
dictionnary_file = options.dicfile

input_dir=''
for i in range (0,len(tex_file.split('\\'))-1):
    input_dir+=tex_file.split('\\')[i]+'\\'
print(input_dir)
# Get argument: a tex file
file_name, file_extension = os.path.splitext(tex_file) 


# Output file name 
if output_file:
    txt_file = output_file    # Name given by user
else:
    txt_file = file_name+'.txt' # If no name add a .txt extension


# Dictionnary file name 
if dictionnary_file:
    dic_file = dictionnary_file    # Name given by user
else:
    dic_file = file_name+'.dic' # If no name add a .dic extension


# Read file object to string
fic_tex = open(tex_file, 'r', encoding='utf-8')
text_all = fic_tex.read()
fic_tex.close()

# Real stuff start there!
# Replacement function pass as the replacement pattern in re.sub()

count = 0           # counter for tags
dictionnary = {}    # memorize tag: key=nb -> value=replacement
def func_repl_input(m):
    """ Function called by sub as replacement pattern given by output
    Input: the pattern to be replaced
    Ouput: the new pattern
    Action: also update the dictionnary of tags/replacement
    and increment the counter
    https://stackoverflow.com/questions/33962371"""
    print(m.group(1))
    global count
    dictionnary[count] = m.group(0)  # Add old string found to the dic
    file=open(input_dir+m.group(1), 'r', encoding='utf-8')
    file_tex=file.read()
    file.close()
    count += 1   
    return file_tex      

def func_repl(m):
    """ Function called by sub as replacement pattern given by output
    Input: the pattern to be replaced
    Ouput: the new pattern
    Action: also update the dictionnary of tags/replacement
    and increment the counter
    https://stackoverflow.com/questions/33962371"""
    global count
    dictionnary[count] = m.group(0)  # Add old string found to the dic
    tag_str = tag+str(count)+tag     # tag = '€' is defined in 'constants.py'
    count += 1   
    return tag_str                   # New string for pattern replacement


# Now we replace case by case math and command by tags
### PART 0 - Replace inputs
text_new = text_all
text_new = re.sub(r'\\input\{(.+?)\}',func_repl_input,text_new, flags=re.MULTILINE|re.DOTALL)


### PART 1 - Replace \begin{env} and \end{env} but not its contents

for env in list_env_discard + list_env_discard_perso:
    print(env)
    str_env = r"\\begin\{" + env + r"\}(.+?)\\end\{" + env + r"\}"
    print(str_env)
    text_new = re.sub(str_env,func_repl,text_new, flags=re.MULTILINE|re.DOTALL)

### PART 2 - Replacement of maths ###

# $$ ... $$
text_new = re.sub(r'\$\$(.+?)\$\$',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
# $ ... $
text_new = re.sub(r'\$(.+?)\$',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
# \( ... \)
text_new = re.sub(r'\\\((.+?)\\\)',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
# \[ ... \]
text_new = re.sub(r'\\\[(.+?)\\\]',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)





### PART 3 - Discards contents of some environnments ###

text_new = re.sub(r'\\begin\{(.+?)\}',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
text_new = re.sub(r'\\end\{(.+?)\}',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)


### PART 4 - Replacement of LaTeX commands with their argument ###

for cmd in list_cmd_arg_discard + list_cmd_arg_discard_perso:
    # Without opt arg, ex. \cmd{arg}
    str_env = r'\\' + cmd + r'\{(.+?)\}'
    text_new = re.sub(str_env,func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
    # With opt arg, ex. \cmd[opt]{arg}
    str_env = r'\\' + cmd + r'\[(.*?)\]\{(.+?)\}'
    text_new = re.sub(str_env,func_repl,text_new, flags=re.MULTILINE|re.DOTALL)


### PART 5 - Replacement of LaTeX remaining commands (but not their argument) ###

text_new = re.sub(r'\\[a-zA-Z]+',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)




# Output: text file
with open(txt_file, 'w', encoding='utf-8') as fic_txt:
    fic_txt.write(text_new)

# Output: dictionnary file
with open(dic_file, 'w', encoding='utf-8') as fic_dic:
    yaml.dump(dictionnary,fic_dic, default_flow_style=False,allow_unicode=True)
