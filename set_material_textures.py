# Script to point all MIs in a list to new textures
# Assumes all MIs point to the same set of textures
# TODO: support cases where different MIs point to different textures

# Usage:
#  - Set your mod dir in mod_dir
#  - list the MIs you want to modify (including the paths, from your mod_dir root) in materials_to_mod
#  - specify the new textures you want each enabled texture slot to point to in texture_nodes_to_replace


import json
import unreal
import importlib

import utils
importlib.reload(utils)

mod_dir = '/your_mod_dir/'

material_util = unreal.MaterialEditingLibrary()

materials_to_mod = [
    mod_dir+'MI_HUM_F_Socks_blublu1',
    mod_dir+'MI_HUM_F_Socks_blacks1',
    mod_dir+'MI_HUM_F_Socks_dblack1',
    mod_dir+'MI_HUM_F_Socks_littan1',
    mod_dir+'MI_HUM_F_Socks_redred1',
    mod_dir+'MI_HUM_F_Socks_suntan1',
    mod_dir+'MI_HUM_F_Socks_whites1'
    ]

#new_material_instance = unreal.load_asset(mod_dir+'MI_HUM_F_Socks_suntan1.MI_HUM_F_Socks_suntan1')

texture_nodes_to_replace = {}

texture_nodes_to_replace['Base_Color'] = mod_dir+'T_HUM_F_Socks_Skin_D'
texture_nodes_to_replace['Base_Normal'] = mod_dir+'T_HUM_F_Socks_Skin_N'
texture_nodes_to_replace['Base_SRO'] = mod_dir+'T_HUM_F_Socks_Socks01_SRO'
texture_nodes_to_replace['Swatch_Diffuse[0]'] = mod_dir+'T_HUM_F_Socks_Skin_D'
texture_nodes_to_replace['Swatch_Diffuse[1]'] = mod_dir+'T_S_Silk_Weave_00_D'
texture_nodes_to_replace['Swatch_MRAB[1]'] = mod_dir+'T_S_Silk_Textured_00_MRAB'
texture_nodes_to_replace['Swatch_Normal[0]'] = mod_dir+'T_HUM_F_Socks_Skin_N'
texture_nodes_to_replace['Swatch_Normal[1]'] = mod_dir+'T_S_Silk_Weave_00_N'


for my_mi_str in materials_to_mod:
    print("Processing "+my_mi_str)
    my_mi = unreal.load_asset(my_mi_str)
    for key, value in texture_nodes_to_replace.items():
        print("Setting texture parameter "+key+" to "+value)
        texture_asset = unreal.load_asset(value)
        material_util.set_material_instance_texture_parameter_value(my_mi, key, texture_asset)
    unreal.EditorAssetLibrary.save_loaded_asset(my_mi, False)