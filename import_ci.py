import unreal
import utils
import importlib
importlib.reload(utils)
from utils import apply, try_create_asset
import json

# Set these next 2 parameters before running the script

# TODO: Set this to root of Content in Fmodel JSON extraction folder
export_root = r"D:\modding\T8_Demo\Exports\Polaris"


# TODO: List the CI assets you want to import
assets_to_import = [

    #'/Content/Character/Item/Customize_Item/kal/bdf/CI_kal_bdf_1p',
    #'/Content/Character/Item/Customize_Item/kal/bdf/CI_kal_bdf_1p_p',
    #'/Content/Character/Item/Customize_Item/kal/bdf/CI_kal_bdf_1p_v1',
    #'/Content/Character/Item/Customize_Item/kal/bdf/CI_kal_bdf_1p_v2',
    #'/Content/Character/Item/Customize_Item/kal/bdf/CI_kal_bdf_2p'
    #'/Content/Character/Item/Customize_Item/cf0/btm/CI_cf0_btm_f_widepants_denim',
    #'/Content/Character/Item/Customize_Item/cf0/btm/CI_cf0_btm_f_hotpants',
    #'/Content/Character/Item/Customize_Item/cf0/btm/CI_cf0_btm_f_mdenim',
    #'/Content/Character/Item/Customize_Item/cf0/bdu/CI_cf0_bdu_f_shirtinss_dot',
    #'/Content/Character/Item/Customize_Item/rat/bdf/CI_rat_bdf_phoenix_dress',
    #'/Content/Character/Item/Customize_Item/cf0/sho/CI_cf0_sho_f_officemule_khA'
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

    asset = try_create_asset(asset_path, asset_name, 'CustomizeItem')
    apply(asset, data)
    unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

    #asset = unreal.CustomizeItem()
    #apply(asset, data)
    #unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(asset_name, asset_path, asset)
    #unreal.EditorAssetLibrary.save_asset(asset_path+asset_name)