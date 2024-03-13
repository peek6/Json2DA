# Generic script to copy and rename Tekken 8 Item Prefab (IP) mods from the UE packaged folder to the LogicMods folder

# Author: peek6

# Usage:
#  - Modify the specified part of the script below as described in the comments
#  - After packaging in UE, run this script as a regular Python script (e.g., from a standard command prompt, not from inside UE)

import os
import shutil
from pathlib import Path

from tekken8_parts_and_chars import chars_dict, body_parts_dict

# My scripts will be using the 600s and 700s for clothing, and the 800s for skin and hair.
from tekken8_chunk_id_assignments import chunk_id_bases

####################################################################################################################

# SPECIFY ALL PARAMETERS BELOW BEFORE RUNNING SCRIPT.  SCRIPT WILL THEN AUTOMATE EVERYTHING ELSE

upper_mod_name = 'your_mod_top'

lower_mod_name = 'your_mod_bottom'

# which types of body parts is your mod going on?  Options are shirts, skirts, pants, coats.
body_parts = ['shirts', 'skirts', 'pants']

# which types of chars is your mod going on?  Options are women, men, alisa, leo, other.
chars_types_to_mod = ['women', 'alisa', 'leo']

pak_src = r"D:\ue_build\polaris_custom_git_proj\Windows\Polaris\Content\Paks"

pak_dest = "D:\SteamLibrary\steamapps\common\TEKKEN 8\Polaris\Content\Paks\LogicMods"

# END OF STUFF YOU NEED TO SPECIFY.  SCRIPT WILL AUTOMATE EVERYTHING ELSE

####################################################################################################################



iostore_exts = ['pak','utoc','ucas']

for body_part in body_parts:
    chunk_id_base = chunk_id_bases[body_part]
    '''
    for current_ext in iostore_exts:
        if body_part == 'coats':
            shutil.copy(pak_src + "\\pakchunk" + str(chunk_id_base) + "-Windows." + current_ext,
                    pak_dest + '\\chunk' + str(chunk_id_base) + '_'+ mod_name +'_for_all_' + body_part+'_P.'+current_ext)
        if body_part == 'pants':
            shutil.copy(pak_src + "\\pakchunk" + str(chunk_id_base) + "-Windows." + current_ext,
                    pak_dest + '\\chunk' + str(chunk_id_base) + '_'+ pants_name +'_for_all_' + body_part+'_P.'+current_ext)
    '''
    body_part_count = 0
    for my_body_part in body_parts_dict[body_part]:
        chunk_id = chunk_id_base + body_part_count
        for current_ext in iostore_exts:
            if body_part == 'coats' or body_part=='shirts':
                shutil.copy(pak_src + "\\pakchunk" + str(chunk_id) + "-Windows." + current_ext,
                    pak_dest + '\\chunk' + str(chunk_id) + '_' + upper_mod_name + '_for_' + my_body_part + '_P.'+current_ext)
            if body_part == 'pants' or body_part=='skirts':
                shutil.copy(pak_src + "\\pakchunk" + str(chunk_id) + "-Windows." + current_ext,
                    pak_dest + '\\chunk' + str(chunk_id) + '_' + lower_mod_name + '_for_' + my_body_part + '_P.'+current_ext)
        body_part_count = body_part_count + 1