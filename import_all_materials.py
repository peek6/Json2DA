# Script to recursively merge all children of all master materials and material instances,
# create all the dummy merged MMs in UE, and then recursively create and populate all material instances.

# Author:  peek6

# Usage:
#  - Use Fmodel to extract all JSON files for all MMs and MIs.
#  - Point json_root to the root of the Content folder in your Fmodel extraction directory
#  - Point texture_root to the root of the Game folder in your Umodel texture extraction directory
#  - Back up all textures in your project
#  - Back up and then delete all materials and material instances in your project
#  - Run this script from inside your UE project


from os import walk
import os
import shutil
import re
import json
from pathlib import Path
from MaterialClasses import Material, MaterialInstance


import importlib
import unreal
import MaterialExpressions
import materialutil
importlib.reload(MaterialExpressions)
importlib.reload(materialutil)

from materialutil import create_ue_material, create_ue_material_instance, recursively_create_material_instances



AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
MEL = unreal.MaterialEditingLibrary
EditorAssetLibrary = unreal.EditorAssetLibrary
EditorUtilityLibrary = unreal.EditorUtilityLibrary
material_util = unreal.MaterialEditingLibrary()


# TODO: Set this to root of Content in Fmodel JSON extraction folder
json_root = r"D:\modding\T8_Demo\Exports\Polaris"

# TODO: Set this to root of Game in Umodel texture extraction folder
texture_root = r"D:\modding\T8\vanilla_textures"


param_types = ['ScalarParameterValues', 'TextureParameterValues', 'VectorParameterValues']

# recursively traverse the Fmodel extraction directory and initialize all the material and material instance objects
def initialize_material_classes():
    p = Path(json_root)

    master_materials = {}
    material_instances = {}

    for file in p.glob('**/M_*.json'):
        json_path = str(file)
        with open(json_path, "r+") as fp:
            global_asset_type = json.load(fp)[0]["Type"]
            tokens = json_path.split('\\')
            asset_name = tokens[-1].split('.')[0]
            tokens_after_content = []
            found_content = False
            for token in tokens[:-1]:
                if (token == 'Content'):
                    found_content = True
                    tokens_after_content.append('Game')
                else:
                    if (found_content):
                        tokens_after_content.append(token)
            asset_path = '/' + '/'.join(tokens_after_content) + '/'
            if(global_asset_type == "Material"):
                new_material = Material(asset_path, asset_name, json_path)
                master_materials[asset_name] = new_material
            elif (global_asset_type == "MaterialInstanceConstant"):
                new_material_instance = MaterialInstance(asset_path, asset_name, json_path)
                material_instances[asset_name] = new_material_instance
                print("WARNING: " + asset_name + " is actually an MI.  Adding it there instead.")
            else:
                print("WARNING: " + asset_name+" is not a Material.  Skipping.")

    for file in p.glob('**/MI_*.json'):
        json_path = str(file)
        tokens = json_path.split('\\')
        asset_name = tokens[-1].split('.')[0]
        tokens_after_content = []
        found_content = False
        for token in tokens[:-1]:
            if (token == 'Content'):
                found_content = True
                tokens_after_content.append('Game')
            else:
                if (found_content):
                    tokens_after_content.append(token)
        asset_path = '/' + '/'.join(tokens_after_content) + '/'
        new_material_instance = MaterialInstance(asset_path, asset_name, json_path)
        material_instances[asset_name] = new_material_instance #.append(new_material_instance)

    return master_materials, material_instances


# recursively merge the material and material instance objects by recursively traversing the tree and merging all children first
def recursively_merge_data(my_node):

    for child_name in my_node.children:
        recursively_merge_data(my_node.children[child_name])
    # do the merging here, so that children get fully merged before parents
    for child_name in my_node.children:
        child_obj = my_node.children[child_name]
        for my_type in param_types:
            # print("Merging " + my_type + " data from child " + child_name + " into parent " + my_node.asset_name)
            for key in child_obj.data_dict[my_type]:
                if key not in my_node.data_dict[my_type]: #TODO:  not sure if I want to be replacing here or not
                    my_node.data_dict[my_type][key] = child_obj.data_dict[my_type][key]
                    # print("Merging "+my_type+" data from child "+child_name+" into parent "+my_node.asset_name)
    return

# Convert the merged data dictionaries back into a list for compatibility with existing methods for constructing MMs and MIs in UE
def data_dict_to_data(my_obj):
    for my_type in param_types:
        if (my_type not in my_obj.data):
            my_obj.data[my_type] = []
        else:
            my_obj.data[my_type].clear()
        for dict_item in my_obj.data_dict[my_type]:
            my_obj.data[my_type].append(my_obj.data_dict[my_type][dict_item])
    return

def main():
    master_materials, material_instances = initialize_material_classes()
    
    # iterate through material instances and populate immediate parents and children
    for mi_name in material_instances:
        # open the JSON file for that material instance as a dict and populate its parent
        mi_obj = material_instances[mi_name]
        with open(mi_obj.json_path, "r+") as fp:
            my_temp = json.load(fp)[0]
            data = my_temp["Properties"]
            global_asset_type = my_temp["Type"]
            # Sanity check that this is actually an MI
            if(global_asset_type == "MaterialInstanceConstant"):
                mi_obj.data = data
                # Convert data list into data dictionary for easier merging (to avoid duplicate parameters)
                for global_my_type in param_types:
                    mi_obj.data_dict[global_my_type] = {}
                    if(global_my_type in data):
                        for list_item in data[global_my_type]:
                            mi_obj.data_dict[global_my_type][list_item["ParameterInfo"]["Name"]] = list_item
                if "SubsurfaceProfile" in data:
                    print("Found SubsurfaceProfile in MI")
                    mi_obj.data_dict["SubsurfaceProfile"] = {}
                    mi_obj.data_dict["SubsurfaceProfile"]["ObjectName"] = mi_obj.data["SubsurfaceProfile"]["ObjectName"]
                    mi_obj.data_dict["SubsurfaceProfile"]["ObjectPath"] = mi_obj.data["SubsurfaceProfile"]["ObjectPath"]
                if 'Parent' in data:
                    if 'ObjectName' in data['Parent']:
                        temp_list = data['Parent']['ObjectName'].split("'")
                        global_my_type = temp_list[0]
                        my_parent_name = temp_list[1]

                        if global_my_type == 'Material':
                            if my_parent_name in master_materials:
                                my_parent_obj = master_materials[my_parent_name]
                                mi_obj.parent = my_parent_obj  # my_parent_name
                                my_parent_obj.children[mi_name] = mi_obj
                            else:
                                print("WARNING:  Cannot find parent material " + my_parent_name + " for MI " + mi_name)
                        elif global_my_type=='MaterialInstanceConstant':
                            if my_parent_name in material_instances:
                                my_parent_obj = material_instances[my_parent_name]
                                mi_obj.parent = my_parent_obj
                                my_parent_obj.children[mi_name] = mi_obj
                            else:
                                print("WARNING:  Cannot find parent material instance " + my_parent_name + " for MI " + mi_name)
                        else:
                            print("WARNING:  Unknown type "+ global_my_type +" for MI " + mi_name)

                    else:
                        print("WARNING:  No parent name for MI " + mi_name)
                else:
                    print("WARNING:  No parent data for MI "+mi_name)
            else:
                print("WARNING: " + mi_name+" is not a MaterialInstanceConstant.  Skipping.")
                del material_instances[mi_name]
    
    
    # For each material, traverse the tree starting from that material as root, and merge
    for mm_name in master_materials:
        mm_obj = master_materials[mm_name]
        for global_my_type in param_types:
            mm_obj.data_dict[global_my_type] = {}
        recursively_merge_data(mm_obj)

    # Convert the merged data dictionaries back into a list for compatibility with existing methods for constructing MMs and MIs in UE
    for mi_name in material_instances:
        data_dict_to_data(material_instances[mi_name])
    
    for mm_name in master_materials:
        data_dict_to_data(master_materials[mm_name])
    
    
    # First create the master material in UE, then recursively create all its child material instances in UE, always creating parents before children

    #mm_name = 'M_CH_skin_V3'
    for mm_name in master_materials:
        mm_obj = master_materials[mm_name]
        print("Creating UE material "+mm_name)
        create_ue_material(mm_obj, texture_root)
        # recursively go through tree for each MM, add parent, then add children.  They are all MIs since I added the MM above.
        for child_name in mm_obj.children:
            mi_obj = mm_obj.children[child_name]
            recursively_create_material_instances(mi_obj, texture_root)

    #create_ue_material_instance(material_instances['MI_CH_kal_face_skin'], texture_root)
    #create_ue_material_instance(material_instances['MI_CH_kal_arm_skin'], texture_root)

    return master_materials, material_instances


master_materials, material_instances = main()



