import importlib
import unreal
import json
import MaterialExpressions
import materialutil
importlib.reload(MaterialExpressions)
importlib.reload(materialutil)
from materialutil import connectNodesUntilSingle
import utils
import MaterialClasses
#import tekken8_import_utils
importlib.reload(utils)
#importlib.reload(tekken8_import_utils)
importlib.reload(MaterialClasses)
importlib.reload(materialutil)
from MaterialClasses import MaterialInstance, Material
from utils import apply, try_create_asset
from materialutil import create_ue_material_instance
#from tekken8_import_utils import generic_tekken8_importer


AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
MEL = unreal.MaterialEditingLibrary
EditorAssetLibrary = unreal.EditorAssetLibrary
EditorUtilityLibrary = unreal.EditorUtilityLibrary

mat = EditorUtilityLibrary.get_selected_assets()[0]

Y_GAP = 175


def create_node(ty, yPos, name, defaultValue, slot_name):
    node = MEL.create_material_expression(mat, ty, 0, yPos * Y_GAP)
    node.set_editor_property("ParameterName", name)
    if defaultValue is not None: node.set_editor_property(slot_name, defaultValue)
    return node

def generateInputNodes(data : dict):
    
    # Store last nodes (not always same as parameter nodes)
    all_final_nodes = []

    for p in data["ScalarParameterValues"]:
        all_final_nodes.append(
            create_node(MaterialExpressions.ScalarParameter, len(all_final_nodes), p["ParameterInfo"]["Name"], p["ParameterValue"], "DefaultValue")
        )

    for p in data["VectorParameterValues"]:
        all_final_nodes.append(
            create_node(MaterialExpressions.VectorParameter, len(all_final_nodes), p["ParameterInfo"]["Name"], unreal.LinearColor(p["ParameterValue"]["R"], p["ParameterValue"]["G"], p["ParameterValue"]["B"], p["ParameterValue"]["A"]), "DefaultValue")
        )

    for p in data["TextureParameterValues"]:

        # print("Processing "+p["ParameterValue"]["ObjectName"])
        if not (p["ParameterValue"] is None):
            obj_type, obj_name = p["ParameterValue"]["ObjectName"].split("'")[:2]
            # print("Received object with type "+obj_type)
            # print("Received object with name "+obj_name)

            print(f"Processing texture {obj_name}...")
            obj_path = p["ParameterValue"]["ObjectPath"]
            print(f"Path={obj_path}")

            full_path = obj_path.split(".")[0] + "." + obj_name
            asset = unreal.load_asset(f"{obj_type}'{full_path}'")

            if asset is None:
                folder = "/".join(obj_path.split(".")[0].split("/")[:-1])
                asset = try_create_asset(folder, obj_name, obj_type)
                print(asset)
                if asset is not None:
                    unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

            slot_name =  p["ParameterInfo"]["Name"]

            print(f"Adding texture {full_path} to slot {slot_name}")

            node = create_node(MaterialExpressions.TextureSampleParameter2D, len(all_final_nodes), p["ParameterInfo"]["Name"], asset, "Texture")

            #node.set_editor_property(slot_name, asset)

            node.set_editor_property("SamplerSource", unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS)

            all_final_nodes.append(
                node
            )


    return all_final_nodes

def import_material_instance(json_path, asset_name, asset_path, texture_root=''):
    print("Running latest MI import")

    with open(json_path, "r+") as fp:
        temp_buffer = json.load(fp)[0]
        if "Properties" in temp_buffer:
            data = temp_buffer["Properties"]
        else:
            print("Warning:  JSON file has no properties to populate")
            data = {}


    mi_obj = MaterialInstance(asset_path, asset_name, json_path)
    mi_obj.data = data
    param_types = ['ScalarParameterValues', 'TextureParameterValues', 'VectorParameterValues']
    # Convert data list into data dictionary for easier merging (to avoid duplicate parameters)
    for global_my_type in param_types:
        mi_obj.data_dict[global_my_type] = {}
        if (global_my_type in data):
            for list_item in data[global_my_type]:
                mi_obj.data_dict[global_my_type][list_item["ParameterInfo"]["Name"]] = list_item

    if "PhysMaterial" in data:
        print("Found PhysMaterial in MI")
        mi_obj.data_dict["PhysMaterial"] = {}
        mi_obj.data_dict["PhysMaterial"]["ObjectName"] = mi_obj.data["PhysMaterial"]["ObjectName"]
        mi_obj.data_dict["PhysMaterial"]["ObjectPath"] = mi_obj.data["PhysMaterial"]["ObjectPath"]

    if "SubsurfaceProfile" in data:
        print("Found SubsurfaceProfile in MI")
        mi_obj.data_dict["SubsurfaceProfile"] = {}
        mi_obj.data_dict["SubsurfaceProfile"]["ObjectName"] = mi_obj.data["SubsurfaceProfile"]["ObjectName"]
        mi_obj.data_dict["SubsurfaceProfile"]["ObjectPath"] = mi_obj.data["SubsurfaceProfile"]["ObjectPath"]

    if 'Parent' in data:
        if 'ObjectPath' in data['Parent']:
            parent_path = ('/').join(data['Parent']['ObjectPath'].split("/")[:-1]) + '/'
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
            print("data_dict is ", "")
            print(mi_obj.data_dict)

            asset_path = mi_obj.asset_path
            asset_name = mi_obj.asset_name

            print("Asset path is " + asset_path)
            print("Asset name is " + asset_name)

            if unreal.EditorAssetLibrary.does_asset_exist(
                    asset_path + '/' + asset_name):  # does_asset_exist(asset_path, asset_name):
                asset = unreal.load_asset(asset_path + '/' + asset_name)  # + '.' + asset_name)
                unreal.EditorAssetLibrary.delete_loaded_asset(asset)  # asset_path + asset_name)

            create_ue_material_instance(mi_obj, texture_root)
            return mi_obj
        else:
            print("WARNING:  No parent name for MI " + asset_name)
    else:
        print("WARNING:  No parent data for MI " + asset_name)


def main(json_path):
    print("=== JSON 2 Material Instance ===")
    # with open(json_path.file_path, "r+") as fp:
    #    data = json.load(fp)[0]["Properties"]
    #data = json.loads(json_path)[0]["Properties"]

    mi_asset = EditorUtilityLibrary.get_selected_assets()[0]
    full_name = mi_asset.get_full_name()
    asset_path = '/'.join(full_name.split(' ')[1].split('/')[:-1]) # full_name.split('.')[0]
    asset_name =  full_name.split(' ')[1].split('/')[-1].split('.')[0]

    print("Running MI importer with JSON path = "+ json_path.file_path + ", asset_name="+asset_name+", asset_path="+asset_path)

    import_material_instance(json_path.file_path, asset_name, asset_path)





    unreal.EditorAssetLibrary.save_loaded_asset(mi_asset, True)


'''
    mi_obj = asset # MaterialInstance(asset_path + '/', asset_name, json_path)
    mi_obj.data = data
    param_types = ['ScalarParameterValues', 'TextureParameterValues', 'VectorParameterValues']
    # Convert data list into data dictionary for easier merging (to avoid duplicate parameters)
    for global_my_type in param_types:
        mi_obj.data_dict[global_my_type] = {}
        if (global_my_type in data):
            for list_item in data[global_my_type]:
                mi_obj.data_dict[global_my_type][list_item["ParameterInfo"]["Name"]] = list_item
    if 'Parent' in data:
        if 'ObjectPath' in data['Parent']:
            parent_path = ('/').join(data['Parent']['ObjectPath'].split("/")[:-1]) + '/'
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
            create_ue_material_instance(mi_obj)
        else:
            print("WARNING:  No parent name for MI " + asset_name)
    else:
        print("WARNING:  No parent data for MI " + asset_name)


    MEL.delete_all_material_expressions(mat)
    nodes = generateInputNodes(data)
    final_node = connectNodesUntilSingle(mat, nodes)
    MEL.connect_material_property(final_node, "", unreal.MaterialProperty.MP_BASE_COLOR)
'''

