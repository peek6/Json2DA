# Sample script to mesh pointers of character piece DA JSONs
# Works by hacking the character piece JSON files, so that the modified JSON files can then be imported using JSON2DA

# TODO:  support searching for different strings in different JSON files

# USAGE:
#  - point to your mod_dir and to the character piece JSONs you want to hack
#  - specify the strings to search for and replace as regular expressions
#  - run the script
#  - use json2da to import the modified JSON files into UE.

import json
#import unreal
#import importlib

#import utils
#importlib.reload(utils)

import re

mod_dir = '/your_mod_name/'

jsons_to_hack = [
    r"D:\modding\hogwarts_legacy\fmodel_hl_extract_2024\Exports\Phoenix\Content\RiggedObjects\Characters\Human\Clothing\Socks_F\Socks01\DA_HUM_F_Socks_Socks01_Master.json",
    r"D:\modding\hogwarts_legacy\fmodel_hl_extract_2024\Exports\Phoenix\Content\RiggedObjects\Characters\Human\Clothing\Socks_F\Socks01\DA_HUM_F_Legs_Legs01_Master.json"
]

for json_file in jsons_to_hack:
    with open(json_file,'r+') as fp:
        buf = fp.read()

    buf = re.sub("\/Game\/RiggedObjects\/Characters\/Human\/Clothing\/Socks_F\/Socks01\/",mod_dir,buf)

    if 'Legs' in json_file:
        with open('legs.json','w+') as fp:
            fp.write(buf)
    else:
        with open('socks.json','w+') as fp:
            fp.write(buf)
