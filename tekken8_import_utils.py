# Generic methods for importing various Tekken 8 assets into UE

# Author: peek6

import unreal
import utils
import importlib
import MaterialClasses
import materialutil
importlib.reload(utils)
importlib.reload(MaterialClasses)
importlib.reload(materialutil)
from MaterialClasses import MaterialInstance, Material
from utils import apply, try_create_asset
from materialutil import create_ue_material_instance
import json

def generic_tekken8_importer(json_path, asset_name, asset_path):
    with open(json_path, "r+") as fp:
        data = json.load(fp)[0]["Properties"]


    if "BEI_" in asset_name:
        asset = try_create_asset(asset_path, asset_name, 'BaseEyeItem')
        apply(asset, data)
        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)
    elif "BMI_" in asset_name:
        asset = try_create_asset(asset_path, asset_name, 'BaseMakeItem')
        apply(asset, data)
        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)
    elif "SBA_" in asset_name:
        asset = unreal.SqueezeBoneAsset()
        apply(asset, data)
        unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(asset_name, asset_path, asset)
        unreal.EditorAssetLibrary.save_asset(asset_path + '/' + asset_name)
    elif "AIP_" in asset_name:
        asset = unreal.AvatarItemPrefab()
        apply(asset, data)
        unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(asset_name, asset_path, asset)
        unreal.EditorAssetLibrary.save_asset(asset_path + '/' + asset_name)
    elif "IP_" in asset_name:
        asset = try_create_asset(asset_path, asset_name, 'ItemPrefab')
        apply(asset, data)
        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)
    elif "CI_" in asset_name:
        asset = try_create_asset(asset_path, asset_name, 'CustomizeItem')
        apply(asset, data)
        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)
    elif "MI_" in asset_name:
        print("Running latest MI import")
        mi_obj = MaterialInstance(asset_path, asset_name, json_path)
        mi_obj.data = data
        param_types = ['ScalarParameterValues', 'TextureParameterValues', 'VectorParameterValues']
        # Convert data list into data dictionary for easier merging (to avoid duplicate parameters)
        for global_my_type in param_types:
            mi_obj.data_dict[global_my_type] = {}
            if (global_my_type in data):
                for list_item in data[global_my_type]:
                    mi_obj.data_dict[global_my_type][list_item["ParameterInfo"]["Name"]] = list_item
        if "SubsurfaceProfile" in data:
            print("Found SubsurfaceProfile in MI")
            mi_obj.data_dict["SubsurfaceProfile"] = {}
            mi_obj.data_dict["SubsurfaceProfile"]["ObjectName"] = mi_obj.data["SubsurfaceProfile"]["ObjectName"]
            mi_obj.data_dict["SubsurfaceProfile"]["ObjectPath"] = mi_obj.data["SubsurfaceProfile"]["ObjectPath"]

        if 'Parent' in data:
            if 'ObjectPath' in data['Parent']:
                parent_path = ('/').join(data['Parent']['ObjectPath'].split("/")[:-1])+'/'
                parent_name = data['Parent']['ObjectPath'].split("/")[-1].split('.')[0]
            else:
                print("WARNING:  No parent path for MI " + asset_name)
            if 'ObjectName' in data['Parent']:
                temp_list = data['Parent']['ObjectName'].split("'")
                global_my_type = temp_list[0]
                my_parent_name = temp_list[1]
                if global_my_type == 'Material':
                    my_parent_obj = Material(parent_path, parent_name, '')
                elif global_my_type == 'MaterialInstanceConstant':
                    my_parent_obj = MaterialInstance(parent_path, parent_name, '')
                else:
                    print("WARNING:  Unknown type " + global_my_type + " for MI " + asset_name)
                mi_obj.parent = my_parent_obj
                print("data_dict is ","")
                print(mi_obj.data_dict)

                asset_path = mi_obj.asset_path
                asset_name = mi_obj.asset_name

                print("Asset path is " + asset_path)
                print("Asset name is " + asset_name)


                if unreal.EditorAssetLibrary.does_asset_exist(asset_path + '/' + asset_name):  # does_asset_exist(asset_path, asset_name):
                    asset = unreal.load_asset(asset_path + '/' + asset_name)  # + '.' + asset_name)
                    unreal.EditorAssetLibrary.delete_loaded_asset(asset)  # asset_path + asset_name)

                create_ue_material_instance(mi_obj)
                return mi_obj
            else:
                print("WARNING:  No parent name for MI " + asset_name)
        else:
            print("WARNING:  No parent data for MI " + asset_name)
    else:
        print("ERROR:  Unknown asset type for asset "+asset_name)
        return


    return



