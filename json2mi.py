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
import tekken8_import_utils
importlib.reload(utils)
importlib.reload(tekken8_import_utils)
importlib.reload(MaterialClasses)
importlib.reload(materialutil)
from MaterialClasses import MaterialInstance, Material
from utils import apply, try_create_asset
from materialutil import create_ue_material_instance
from tekken8_import_utils import generic_tekken8_importer


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



def main(json_path):
    print("=== JSON 2 Material Instance ===")
    # with open(json_path.file_path, "r+") as fp:
    #    data = json.load(fp)[0]["Properties"]
    #data = json.loads(json_path)[0]["Properties"]

    mi_asset = EditorUtilityLibrary.get_selected_assets()[0]
    full_name = mi_asset.get_full_name()
    asset_path = '/'.join(full_name.split(' ')[1].split('/')[:-1]) # full_name.split('.')[0]
    asset_name =  full_name.split(' ')[1].split('/')[-1].split('.')[0]

    print("Running generic_tekken8_importer import with JSON path = "+ json_path.file_path + ", asset_name="+asset_name+", asset_path="+asset_path)

    generic_tekken8_importer(json_path.file_path, asset_name, asset_path)
    unreal.EditorAssetLibrary.save_loaded_asset(mi_asset, False)


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

