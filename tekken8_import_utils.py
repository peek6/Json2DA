import unreal
import utils
import importlib
importlib.reload(utils)
from utils import apply
import json

def generic_tekken8_importer(json_path, asset_name, asset_path):
    with open(json_path, "r+") as fp:
        data = json.load(fp)[0]["Properties"]

    if "CI_" in asset_name:
        design_assign_slot_array = data['DesignAssignSlotArray']
        assign_pre_material_array =  data['AssignPerMaterialArray']
        asset = unreal.CustomizeItem()
    elif "SBA_" in asset_name:
        asset = unreal.SqueezeBoneAsset()
    else:
        print("ERROR:  Unknown asset type for asset "+asset_name)
        return

    apply(asset, data)

    unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(asset_name, asset_path, asset)
    unreal.EditorAssetLibrary.save_asset(asset_path+asset_name)
    return



