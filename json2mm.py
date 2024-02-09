import importlib
import unreal
import json
import MaterialExpressions
import materialutil
importlib.reload(MaterialExpressions)
importlib.reload(materialutil)
from materialutil import connectNodesUntilSingle
from utils import try_create_asset

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

        obj_type, obj_name = p["ParameterValue"]["ObjectName"].split("'")[:2]
        
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
    with open(json_path.file_path, "r+") as fp:
        data = json.load(fp)[0]["Properties"]
    #data = json.loads(json_path)[0]["Properties"]

    MEL.delete_all_material_expressions(mat)
    nodes = generateInputNodes(data)
    final_node = connectNodesUntilSingle(mat, nodes)
    MEL.connect_material_property(final_node, "", unreal.MaterialProperty.MP_BASE_COLOR)
    unreal.EditorAssetLibrary.save_loaded_asset(mat, True)
