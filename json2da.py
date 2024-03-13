import json
import unreal
import importlib

import utils
importlib.reload(utils)

from utils import apply


def main(json_path):
    print("=== JSON 2 T8 ASSET ===")
    sel_asset = unreal.EditorUtilityLibrary.get_selected_assets()
    with open(json_path.file_path, "r+") as fp:
        data = json.load(fp)[0]["Properties"]
        [apply(asset, data) for asset in sel_asset]
        for asset in sel_asset:
            unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

'''
def main(json_string):
    print("=== JSON 2 T8 ASSET ===")
    sel_asset = unreal.EditorUtilityLibrary.get_selected_assets()
    data = json.loads(json_string)[0]
    [apply(asset, data["Properties"]) for asset in sel_asset]
    for asset in sel_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)
'''