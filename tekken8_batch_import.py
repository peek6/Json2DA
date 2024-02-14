# UE Python script to batch import Tekken8 assets from Fmodel JSON files by type
# Author:  peek6

# Usage:
# Extract all JSON files using Fmodel
# Set export_root to the root (e.g., parent dir) of Content in your Fmodel JSON extraction folder
# List the prefixes for the types you want to import in types_to_import (e.g., SBA, CI, etc.)
# Currently supports batch importing SBA and CI files
# Known issues:  very slow and prone to crash UE.  TODO:  Convert to using factories
# Highly recommend deleting all files of the target type from your project before running this script or UE will ask if you want to replace each one.

from pathlib import Path


import unreal
import utils
import tekken8_import_utils
import importlib
importlib.reload(utils)
importlib.reload(tekken8_import_utils)
from utils import apply
import json


def main():
    # Set these next 2 parameters before running the script

    # TODO: Set this to root of Content in Fmodel JSON extraction folder
    export_root = r"D:\modding\T8_Demo\Exports\Polaris"

    #TODO:  Set file types to import
    types_to_import = ['SBA']

    p = Path(export_root)

    assets_to_import = []
    type_idx = {}

    # TODO: List the assets you want to import.  Currently, CI and SBA are supported
    global_idx=0
    for type_to_import in types_to_import:
        # Import all JSON files of this type
        type_idx[type_to_import]=0
        for file in p.glob('**/'+type_to_import+'_*.json'):
            json_path = str(file)
            tokens = json_path.split('\\')
            asset_name = tokens[-1].split('.')[0]
            tokens_after_content = []
            found_content=False
            for token in tokens[:-1]:
                if(token=='Content'):
                    found_content = True
                    tokens_after_content.append('Game')
                else:
                    if(found_content):
                        tokens_after_content.append(token)
            asset_path = '/'+'/'.join(tokens_after_content)+'/'
            print("Importing " + json_path +" into "+asset_path+asset_name)
            tekken8_import_utils.generic_tekken8_importer(json_path, asset_name, asset_path)
            type_idx[type_to_import] = type_idx[type_to_import]+1
            global_idx = global_idx+1

    for type_to_import in types_to_import:
        print("Imported " + str(type_idx[type_to_import]) + " "+type_to_import+" assets.")
    print("Imported a total of "+str(global_idx)+" assets.")
            #if(idx==1):
            #    return
            #print(asset_path)
            #print(asset_name)

            # print(file)





'''
    assets_to_import.append(
        '/Content/Character/Item/Customize_Item/cf0/sho/CI_cf0_sho_f_furshortboots'
        # '/Content/Character/Item/Customize_Item/cf0/bdu/CI_cf0_bdu_f_shirtinss_dot',
        # '/Content/Character/Item/Customize_Item/mnt/bdu/CI_mnt_bdu_f_shirtinss_dot'

        # '/Content/Character/Item/Customize_Item/cf0/sho/CI_cf0_sho_f_sandals'
        # '/Content/Character/Item/Customize_Item/cf0/bdu/CI_cf0_bdu_f_mlongcoat_houndstooth'
        # '/Content/Character/Item/Customize_Item/zbr/bdf/CI_zbr_bdf_1p'
        # '/Content/Character/Item/Customize_Item/cf0/btm/CI_cf0_btm_f_widepants_denim',
        # '/Content/Character/Item/Customize_Item/cf0/btm/CI_cf0_btm_f_hotpants',
        # '/Content/Character/Item/Customize_Item/cf0/btm/CI_cf0_btm_f_mdenim',

        # '/Content/Character/Item/Customize_Item/rat/bdf/CI_rat_bdf_phoenix_dress',
        # '/Content/Character/Item/Customize_Item/cf0/sho/CI_cf0_sho_f_officemule_khA'
        ]

    for asset_to_import in assets_to_import:
        asset_name = asset_to_import.split('/')[-1]
        editor_asset_path = '/'.join(asset_to_import.split('/')[:-1])

        asset_path = '/Game'+"/"+("/").join(editor_asset_path.split('/')[2:]) + '/'
        json_path = export_root + ("\\").join(editor_asset_path.split('/')) + ("\\") + asset_name + ".json"
        tekken8_import_utils.generic_tekken8_importer(json_path, asset_name, asset_path)
'''

main()


