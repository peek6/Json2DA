import json
import unreal
import utils
import importlib
importlib.reload(utils)
from utils import apply

def main(json_path):
    print("=== IMPORT SBA ===")
    with open(json_path.file_path, "r+") as fp:
        data = json.load(fp)[0]["Properties"]

    sel_asset = unreal.EditorUtilityLibrary.get_selected_assets()

    for asset in sel_asset:
        # asset = unreal.SqueezeBoneAsset()
        utils.apply(asset, data)
        # asset.set_editor_property('squeeze_bone_data_array', my_dict)
        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)