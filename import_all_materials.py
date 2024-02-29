# Script to recursively merge all children of all master materials and material instances,
# create all the dummy merged MMs in UE, and then recursively create and populate all material instances.

# Author:  peek6

# Usage:
#  - Use Fmodel to extract all JSON files for all MMs and MIs.
#  - Point export_root to the root of the Content folder in your Fmodel extraction directory
#  - Back up all textures in your project
#  - Back up and then delete all materials and material instances in your project
#  - Run this script from inside your UE project


from os import walk
import os
import shutil
import re
import json
from pathlib import Path


import importlib
import unreal
import MaterialExpressions
import materialutil
importlib.reload(MaterialExpressions)
importlib.reload(materialutil)

from materialutil import connectNodesUntilSingle, generateInputNodes_modular
from utils import try_create_asset

AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
MEL = unreal.MaterialEditingLibrary
EditorAssetLibrary = unreal.EditorAssetLibrary
EditorUtilityLibrary = unreal.EditorUtilityLibrary
material_util = unreal.MaterialEditingLibrary()


# TODO: Set this to root of Content in Fmodel JSON extraction folder
export_root = r"D:\modding\T8_Demo\Exports\Polaris"

param_types = ['ScalarParameterValues', 'TextureParameterValues', 'VectorParameterValues']

class Material:
    def __init__(self, asset_path, asset_name, json_path):
        self.asset_path = asset_path
        self.asset_name = asset_name
        self.asset_type = 'Material'
        self.json_path = json_path
        self.children = {} # dictionary keyed by asset name of the immediate children of this material
        self.data = {} # data list of parameters compatible with method to create the material in UE
        self.data_dict = {} # data dictionary of parameters for easier merging (to avoid duplicate parameters)

class MaterialInstance:
    def __init__(self, asset_path, asset_name, json_path):
        self.asset_path = asset_path
        self.asset_name = asset_name
        self.asset_type = 'MaterialInstanceConstant'
        self.json_path = json_path
        self.children = {}  # dictionary keyed by asset name of the immediate children of this material instance
        self.parent = None # pointer to parent object of this MI
        self.data = {} # data list of parameters compatible with method to create the material instance in UE
        self.data_dict = {} # data dictionary of parameters for easier merging (to avoid duplicate parameters)


def load_texture(obj_path, obj_name):
    obj_type = "Texture2D"
    full_path = obj_path + obj_name + "." + obj_name
    return unreal.load_asset(f"{obj_type}'{full_path}'")

def load_mi(obj_path, obj_name):
    obj_type = "MaterialInstanceConstant"
    full_path = obj_path + obj_name + "." + obj_name
    return unreal.load_asset(f"{obj_type}'{full_path}'")

def load_material(obj_path, obj_name):
    obj_type = "Material"
    full_path = obj_path + obj_name + "." + obj_name
    return unreal.load_asset(f"{obj_type}'{full_path}'")

# Create the dummy master material in UE from the merged master material object
def create_ue_material(mm_obj):

    mat = try_create_asset(mm_obj.asset_path, mm_obj.asset_name, 'Material')

    data = mm_obj.data

    MEL.delete_all_material_expressions(mat)
    nodes = generateInputNodes_modular(mat,data)
    final_node = connectNodesUntilSingle(mat, nodes)
    if final_node is not None:
        MEL.connect_material_property(final_node, "", unreal.MaterialProperty.MP_BASE_COLOR)
    else:
        print("WARNING: There are no parameters in Material "+mm_obj.asset_name)
    unreal.EditorAssetLibrary.save_loaded_asset(mat, False)

# Create the material instance in UE from the merged material instance object
def create_ue_material_instance(mi_obj):

    my_mi = try_create_asset(mi_obj.asset_path, mi_obj.asset_name, 'MaterialInstanceConstant')


    # set parent
    parent_obj = mi_obj.parent
    if parent_obj is not None:
        #parent_name = parent_obj.asset_name
        if parent_obj.asset_type == 'Material': #parent_name in master_materials:
            #parent_obj = master_materials[parent_name]
            parent_mi = load_material(parent_obj.asset_path, parent_obj.asset_name)
            material_util.set_material_instance_parent(my_mi, parent_mi)
        elif parent_obj.asset_type == 'MaterialInstanceContent': # parent_name in material_instances:
            # parent_obj = material_instances[parent_name]
            parent_mi = load_mi(parent_obj.asset_path, parent_obj.asset_name)
            material_util.set_material_instance_parent(my_mi, parent_mi)
        else:
            print("WARNING:  Parent object has invalid asset type "+parent_obj.asset_type+" for MI " + mi_obj.asset_name)
    else:
        print("WARNING:  No parent set for MI " + mi_obj.asset_name)

    data_dict = mi_obj.data_dict

    # set ScalarParameterValues
    for key in data_dict['ScalarParameterValues']:
        if 'ParameterValue' in data_dict['ScalarParameterValues'][key]:
            material_util.set_material_instance_scalar_parameter_value(my_mi, key, data_dict['ScalarParameterValues'][key]['ParameterValue'])
        else:
            print("WARNING:  Scalar Parameter Value for "+key+" not found in MI " + mi_obj.asset_name)

    # set VectorParameterValues
    for key in data_dict['VectorParameterValues']:
        if 'ParameterValue' in data_dict['VectorParameterValues'][key]:
            dict_with_rgba = data_dict['VectorParameterValues'][key]['ParameterValue']
            material_util.set_material_instance_vector_parameter_value(my_mi, key, unreal.LinearColor(r=dict_with_rgba['R'], g=dict_with_rgba['G'], b=dict_with_rgba['B'], a=dict_with_rgba['A']))
        else:
            print("WARNING:  Vector Parameter Value for "+key+" not found in MI " + mi_obj.asset_name)

    # set TextureParameterValues
    for key in data_dict['TextureParameterValues']:
        p = data_dict['TextureParameterValues'][key]
        if 'ParameterValue' in p:
            if not (p["ParameterValue"] is None):
                obj_type, obj_name = p["ParameterValue"]["ObjectName"].split("'")[:2]
                # print("Received object with type "+obj_type)
                # print("Received object with name "+obj_name)

                #print(f"Processing texture {obj_name}...")
                obj_path = p["ParameterValue"]["ObjectPath"]
                #print(f"Path={obj_path}")

                full_path = obj_path.split(".")[0] + "." + obj_name
                asset = unreal.load_asset(f"{obj_type}'{full_path}'")

                if asset is None:
                    folder = "/".join(obj_path.split(".")[0].split("/")[:-1])
                    asset = try_create_asset(folder, obj_name, obj_type)
                    #print(asset)
                    if asset is not None:
                        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

                # slot_name = p["ParameterInfo"]["Name"]

                #print(f"Adding texture {full_path} to slot {slot_name}")

                material_util.set_material_instance_texture_parameter_value(my_mi, key , asset)
            else:
                print("WARNING:  Texture Parameter Value for "+key+" not found in MI " + mi_obj.asset_name)



    unreal.EditorAssetLibrary.save_loaded_asset(my_mi, False)
    return

# recursively create all material instances in UE, creating parents before children
def recursively_create_material_instances(mi_obj):

    # create instance for parent
    create_ue_material_instance(mi_obj)
    # recursively create instances for children
    for child_name in mi_obj.children:
        recursively_create_material_instances(mi_obj.children[child_name])
    return

# recursively traverse the Fmodel extraction directory and initialize all the material and material instance objects
def initialize_material_classes():
    p = Path(export_root)

    master_materials = {}
    material_instances = {}

    for file in p.glob('**/M_*.json'):
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
        new_material = Material(asset_path, asset_name, json_path)
        master_materials[asset_name] = new_material # .append(new_material)

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
            data = json.load(fp)[0]["Properties"]
            mi_obj.data = data
            # Convert data list into data dictionary for easier merging (to avoid duplicate parameters)
            for global_my_type in param_types:
                mi_obj.data_dict[global_my_type] = {}
                if(global_my_type in data):
                    for list_item in data[global_my_type]:
                        mi_obj.data_dict[global_my_type][list_item["ParameterInfo"]["Name"]] = list_item
    
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
    for mm_name in master_materials:
        mm_obj = master_materials[mm_name]
        create_ue_material(mm_obj)
        # recursively go through tree for each MM, add parent, then add children.  They are all MIs since I added the MM above.
        for child_name in mm_obj.children:
            mi_obj = mm_obj.children[child_name]
            recursively_create_material_instances(mi_obj)

main()



