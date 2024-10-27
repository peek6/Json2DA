import unreal
import utils
import importlib
importlib.reload(utils)
from utils import apply
import json

# Set these next 2 parameters before running the script

# TODO: Set this to root of Content in Fmodel JSON extraction folder
export_root = r"D:\modding\T8_Demo\Exports\Polaris"


# TODO: List the CI assets you want to import
assets_to_import = [
    '/Content/Character/Item/shared/skeleton/DYB_CH_female_bust',
    '/Content/Character/Item/model/unique/KAL/full_body/kal_bdf_1p/meshes/DYB_CH_kal_bdf_1p_bust'
]

for asset_to_import in assets_to_import:
    asset_name = asset_to_import.split('/')[-1]
    editor_asset_path = '/'.join(asset_to_import.split('/')[:-1])

    asset_path = '/Game'+"/"+("/").join(editor_asset_path.split('/')[2:]) + '/'
    json_path = export_root + ("\\").join(editor_asset_path.split('/')) + ("\\") + asset_name + ".json"

    with open(json_path, "r+") as fp:
        data = json.load(fp)[0]["Properties"]

    #design_assign_slot_array = data['DesignAssignSlotArray']
    #assign_pre_material_array =  data['AssignPerMaterialArray']


    asset = unreal.PhoenixDynamicBoneBinary()
    apply(asset, data)

    unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(asset_name, asset_path, asset)
    unreal.EditorAssetLibrary.save_asset(asset_path+asset_name)