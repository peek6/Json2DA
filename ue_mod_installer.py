#  Script to automate chunk copying/renaming for Tekken 8
#  Author: peek6

# Usage:

# 1) Point ue_pak_dir to the location where UE sticks its packaged chunks
# 2) Point mod_dir to the location of your Tekken 8 LogicMods folder
# 3) Specify the chunks IDs for your mod in chunks_to_install
# 4) Run the script, which will copy the mod to LogicMods and rename the files to end in _P

import shutil

# Specify these 3
ue_pak_dir = r'c:\ue_build\polaris_custom_git_proj\Windows\Polaris\Content\Paks'
#ue_pak_dir = r'D:\polar_project_custom_git\Saved\StagedBuilds\Windows\Polaris\Content\Paks'
mod_dir = r'C:\Program Files (x86)\Steam\steamapps\common\TEKKEN 8\Polaris\Content\Paks\LogicMods'
chunks_to_install = [781, 1295] # [591, 592, 593, 598, 1295] # [734, 1772] # [751, 752, 753, 754, 755, 756, 757, 758, 759, 1171, 1771] #[783] # , 789, 1001] # [784, 793, 794, 795] # [249] # [591, 592, 598, 789, 1024] # [786, 787, 788, 789] # [592, 598, 786, 787, 788, 789, 1024]# [1048] # 593, 598, 1048] # [593] # , 1001]#  [20, 791, 794, 796, 598] # , 852]# [654, 790, 791, 792, 793, 794, 795, 895, 896] #[895, 896, 954] #  Example:  [10, 11, 190, 194, 195, 196, 250, 295, 296, 299]


exts = ['.utoc','.ucas','.pak']

for chunk in chunks_to_install:
    for ext in exts:
        src = ue_pak_dir + '\pakchunk'+str(chunk)+'-Windows'+ext
        dst = mod_dir + '\pakchunk'+str(chunk)+'-Windows_P'+ext
        shutil.copyfile(src,dst)
