#  Script to automate chunk copying/renaming for Tekken 8
#  Author: peek6

# Usage:

# 1) Point ue_pak_dir to the location where UE sticks its packaged chunks
# 2) Point mod_dir to the location of your Tekken 8 LogicMods folder
# 3) Specify the chunks IDs for your mod in chunks_to_install
# 4) Run the script, which will copy the mod to LogicMods and rename the files to end in _P

import shutil

# Specify these 3
ue_pak_dir = r'D:\ue_build\polaris_custom_git_proj\Windows\Polaris\Content\Paks'
mod_dir = r'D:\SteamLibrary\steamapps\common\TEKKEN 8\Polaris\Content\Paks\LogicMods'
chunks_to_install = [] # [593] # , 1001]#  [20, 791, 794, 796, 598] # , 852]# [654, 790, 791, 792, 793, 794, 795, 895, 896] #[895, 896, 954] #  Example:  [10, 11, 190, 194, 195, 196, 250, 295, 296, 299]


exts = ['.utoc','.ucas','.pak']

for chunk in chunks_to_install:
    for ext in exts:
        src = ue_pak_dir + '\pakchunk'+str(chunk)+'-Windows'+ext
        dst = mod_dir + '\pakchunk'+str(chunk)+'-Windows_P'+ext
        shutil.copyfile(src,dst)