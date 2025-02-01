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
#import tekken8_import_utils
import importlib
importlib.reload(utils)
#importlib.reload(tekken8_import_utils)
from utils import apply
import json

import ff7rebirth_import_utils
importlib.reload(ff7rebirth_import_utils)
from ff7rebirth_import_utils import mi_importer

def main():
    # Set these next 2 parameters before running the script

    # TODO: Set this to root of Content in Fmodel JSON extraction folder
    json_root = r"D:\modding\ff7r_2\Exports\End\Content\Character\Player"

    # TODO: Set this to root of Game in Umodel texture extraction folder
    texture_root = r"D:\modding\ff7r_2"

    p = Path(json_root)

    for file in p.glob('**/Material/*.json'):
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
        my_mi = mi_importer(json_path, asset_name, asset_path, texture_root)
        unreal.EditorAssetLibrary.save_loaded_asset(my_mi, False)

        # tekken8_import_utils.generic_tekken8_importer(json_path, asset_name, asset_path, texture_root)



    #for type_to_import in types_to_import:
    #    print("Imported " + str(type_idx[type_to_import]) + " "+type_to_import+" assets.")
    #print("Imported a total of "+str(global_idx)+" assets.")


main()


