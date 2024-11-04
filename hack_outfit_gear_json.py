# Sample script to modify location of character piece DAs pointed to by outfit gear DAs.
# Works by hacking the JSON files for the gear DAs, so that the modified JSON files can then be bulk imported by mass_import.py

# USAGE:
#  - point to your mod_dir and to the original and new gear DA JSON paths
#  - specify the strings to search for and replace as regular expressions
#  - run the script
#  - use mass_import.py to batch import the modified JSON files into UE.

import json
from pathlib import Path
#import unreal
#import importlib

#import utils
#importlib.reload(utils)

import re

mod_dir = '/your_mod_name/'

old_gear_json_root = r"D:\games\tools\FModel\Output\Exports\Phoenix\Content\Data\GearAppearances\Outfit\Modded"
new_gear_json_root = r"D:\games\tools\FModel\Output\Exports\Phoenix\Content\Data\GearAppearances\Outfit\Modded_Creator_Kit"

p = Path(old_gear_json_root)

for file in p.glob('**/*.json'):
    json_path = str(file)
    with open(json_path, "r+") as fp:
        buf = fp.read()

    buf = re.sub('/Game/RiggedObjects/Characters/Human/Clothing/Socks_F/Socks01/DA_HUM_F_Socks_Socks01_Master', mod_dir+'DA_HUM_F_Socks_Socks01_Master', buf)
    buf = re.sub('/Game/RiggedObjects/Characters/Human/Clothing/Lower_F/Dress_StuUni01/DA_HUM_F_Low_StuUni01_Master', mod_dir+'DA_HUM_F_Low_StuUni01_Master', buf)
    buf = re.sub('/Game/RiggedObjects/Characters/Human/Clothing/Lower_F/Dress_StuUni03/DA_HUM_F_Low_StuUni03_Master', mod_dir+'DA_HUM_F_Low_StuUni03_Master', buf)

    temp = json_path.split('\\')
    old_file_path = temp[:-1]
    filename = temp[-1]
    new_file_path = new_gear_json_root+'\\'+filename
    print(new_file_path)
    with open(new_file_path, "w+") as fp:
        fp.write(buf)