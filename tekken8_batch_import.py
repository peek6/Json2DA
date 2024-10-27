# UE Python script to batch import Tekken8 assets from Fmodel JSON files by type
# Author:  peek6

# Usage:
# Extract all JSON files using Fmodel
# Set export_root to the root (e.g., parent dir) of Content in your Fmodel JSON extraction folder
# List the prefixes for the types you want to import in types_to_import (e.g., SBA, CI, BEI, BMI, etc.)
# Currently supports batch importing SBA, CI, and BEI files.  Other types (such as BMI) might work but not yet tested.
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

    # TODO: Set this to root of Game in Umodel texture TGA extraction folder
    texture_root = r"D:\modding\T8\vanilla_textures"

    # TODO: Set this to root of Content in Fmodel JSON extraction folder, or to the root folder for the assets you want to batch import
    export_root = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item"

    #TODO:  Set file types to import
    types_to_import = ['DYB_CH']

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
            asset_path = '/'+'/'.join(tokens_after_content) #+'/'
            print("Importing " + json_path +" into "+asset_path+asset_name)
            tekken8_import_utils.generic_tekken8_importer(json_path, asset_name, asset_path, texture_root)
            type_idx[type_to_import] = type_idx[type_to_import]+1
            global_idx = global_idx+1

    for type_to_import in types_to_import:
        print("Imported " + str(type_idx[type_to_import]) + " "+type_to_import+" assets.")
    print("Imported a total of "+str(global_idx)+" assets.")


main()


