# UE Python script to import individual Tekken8 assets from your Fmodel JSON files by specifying their JSON paths.
# Paths must include "Content\Character\..."
# Author:  peek6

# Usage:
# Extract your JSON files using Fmodel
# List the json files you want to import in json_paths in the format shown (e.g., r"your_full_path/your_file.json").  Paths must include "Content\Character\..."
# Currently supports importing SBA and CI files
# Known issues:  very slow and prone to crash UE.  TODO:  Convert to using factories
# If the assets you are importing already exist in UE, I highly recommend deleting them before running this script or UE will ask if you want to replace each one and wll likely crash.

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
    # TODO: Set this before running the script
    json_paths = [
        r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\Customize_Item\cf0\bdu\CI_cf0_bdu_f_mlongcoat_herringbone.json",
        ]
    for json_path in json_paths:
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

main()


