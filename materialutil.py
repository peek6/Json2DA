from pathlib import Path

import unreal
import MaterialExpressions

from utils import try_create_asset
from MaterialClasses import Material, MaterialInstance

MEL = unreal.MaterialEditingLibrary
material_util = unreal.MaterialEditingLibrary()

def create_named_parameter(mat, name, ty, x, y):
    node = MEL.create_material_expression(mat, ty, x, y)
    node.set_editor_property("ParameterName", name)
    return node 

def create_parameter_array(mat, name, ty, num, originX = 0, originY = 0, X_SPACE=0, Y_SPACE=250):
    nodes = [
        create_named_parameter(mat, f"{name}[{i}]", ty, originX + X_SPACE * i, originY + Y_SPACE * i)
        for i in range(1, num + 1)
    ]
    return nodes

def getScalarOutput(node):
    if isinstance(node, (MaterialExpressions.TextureSampleParameter2D, MaterialExpressions.VectorParameter)):
        return "R"

    return ""
    

def connectNodesUntilSingle(mat, _nodes : list):
    nodes = [*_nodes]

    y = 0

    while len(nodes) > 1:
        nodeA, nodeB = nodes[:2]
        nodes = nodes[2:]
        connector = MEL.create_material_expression(mat, MaterialExpressions.Add, 200, y)
        MEL.connect_material_expressions(nodeA, getScalarOutput(nodeA), connector, "A")
        MEL.connect_material_expressions(nodeB, getScalarOutput(nodeB), connector, "B")
        nodes.append(connector)
        y += 75

    if not nodes:
        return None #  print("WARNING: There are no nodes in Material")
    else:
        return nodes[0]


# filename: str : Windows file fullname of the asset you want to import
# destination_path: str : Asset path
# option: obj : Import option object. Can be None for assets that does not usually have a pop-up when importing. (e.g. Sound, Texture, etc.)
# return: obj : The import task object
def buildImportTask(filename='', destination_path='', destination_name='', options=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', destination_name)
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.set_editor_property('options', options)
    return task

def create_texture_with_factory(folder, name, clazz, factory_name):
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = getattr(unreal, factory_name)()
    # print(factory)
    return tools.create_asset(name, folder, clazz, factory)


def try_create_texture(folder, name, type_str, windows_texture_path=''):
    #my_path = (texture_root + ('\\').join(z.split('/'))).split('.')[0] + '.tga'
    if not hasattr(unreal, type_str):
        unreal.log_error(f"{type_str} does not exist")
        return

    clazz = getattr(unreal, type_str)
    assert(clazz=='Texture2D')
    factory_name = 'Texture2DFactoryNew'

    try:
        asset = create_texture_with_factory(folder, name, clazz, factory_name)
        if asset is not None: return asset
    except Exception as e:
        unreal.log_error(e)

    return None


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

def create_node_modular(mat, ty, yPos, name, defaultValue, slot_name):
    Y_GAP = 175
    node = MEL.create_material_expression(mat, ty, 0, yPos * Y_GAP)
    node.set_editor_property("ParameterName", name)
    if defaultValue is not None: node.set_editor_property(slot_name, defaultValue)
    return node


def generateInputNodes_modular(mat, data: dict, texture_root=''):
    # Store last nodes (not always same as parameter nodes)
    all_final_nodes = []

    for p in data["ScalarParameterValues"]:
        all_final_nodes.append(
            create_node_modular(mat, MaterialExpressions.ScalarParameter, len(all_final_nodes), p["ParameterInfo"]["Name"],
                        p["ParameterValue"], "DefaultValue")
        )

    for p in data["VectorParameterValues"]:
        all_final_nodes.append(
            create_node_modular(mat, MaterialExpressions.VectorParameter, len(all_final_nodes), p["ParameterInfo"]["Name"],
                        unreal.LinearColor(p["ParameterValue"]["R"], p["ParameterValue"]["G"], p["ParameterValue"]["B"],
                                           p["ParameterValue"]["A"]), "DefaultValue")
        )

    for p in data["TextureParameterValues"]:

        # print("Processing "+p["ParameterValue"]["ObjectName"])
        if not (p["ParameterValue"] is None):
            obj_type, obj_name = p["ParameterValue"]["ObjectName"].split("'")[:2]
            # print("Received object with type "+obj_type)
            # print("Received object with name "+obj_name)

            #print(f"Processing texture {obj_name}...")
            obj_path = p["ParameterValue"]["ObjectPath"]
            windows_texture_path = (texture_root+('\\').join(obj_path.split('/'))).split('.')[0]+'.tga'
            #print(f"Path={obj_path}")
            #print(f"windows_texture_path={windows_texture_path}")

            full_path = obj_path.split(".")[0] + "." + obj_name
            asset = unreal.load_asset(f"{obj_type}'{full_path}'")

            if asset is None:
                folder = "/".join(obj_path.split(".")[0].split("/")[:-1])
                if (Path(windows_texture_path).is_file()):
                    #print("Importing texture at " + windows_texture_path)
                    my_task = buildImportTask(windows_texture_path, folder)
                    tasks = [my_task]
                    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
                    asset = unreal.load_asset(f"{obj_type}'{full_path}'")
                else:
                    asset = try_create_asset(folder, obj_name, obj_type)
                #print(asset)
                if asset is not None:
                    unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

            slot_name = p["ParameterInfo"]["Name"]

            #print(f"Adding texture {full_path} to slot {slot_name}")

            node = create_node_modular(mat, MaterialExpressions.TextureSampleParameter2D, len(all_final_nodes),
                               p["ParameterInfo"]["Name"], asset, "Texture")

            # node.set_editor_property(slot_name, asset)

            node.set_editor_property("SamplerSource", unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS)

            all_final_nodes.append(
                node
            )

    return all_final_nodes

# Create the dummy master material in UE from the merged master material object
def create_ue_material(mm_obj, texture_root=''):

    mat = try_create_asset(mm_obj.asset_path, mm_obj.asset_name, 'Material')

    data = mm_obj.data

    MEL.delete_all_material_expressions(mat)
    nodes = generateInputNodes_modular(mat,data, texture_root)
    final_node = connectNodesUntilSingle(mat, nodes)
    if final_node is not None:
        MEL.connect_material_property(final_node, "", unreal.MaterialProperty.MP_BASE_COLOR)
    else:
        print("WARNING: There are no parameters in Material "+mm_obj.asset_name)
    unreal.EditorAssetLibrary.save_loaded_asset(mat, False)

# Create the material instance in UE from the merged material instance object
def create_ue_material_instance(mi_obj, texture_root=''):


    my_mi = try_create_asset(mi_obj.asset_path, mi_obj.asset_name, 'MaterialInstanceConstant')

    print("Populating MI at "+my_mi.get_full_name())

    # set parent
    parent_obj = mi_obj.parent
    if parent_obj is not None:
        #parent_name = parent_obj.asset_name
        if parent_obj.asset_type == 'Material': #parent_name in master_materials:
            #parent_obj = master_materials[parent_name]
            parent_mi = load_material(parent_obj.asset_path, parent_obj.asset_name)
            print("Setting parent of " + mi_obj.asset_name + " = " + parent_obj.asset_path + parent_obj.asset_name)
            print(parent_mi)
            material_util.set_material_instance_parent(my_mi, parent_mi)
        elif parent_obj.asset_type == 'MaterialInstanceConstant': # parent_name in material_instances:

            # parent_obj = material_instances[parent_name]
            parent_mi = load_mi(parent_obj.asset_path, parent_obj.asset_name)
            print("Setting parent of " + mi_obj.asset_name + " = " + parent_obj.asset_path + parent_obj.asset_name)
            print(parent_mi)
            material_util.set_material_instance_parent(my_mi, parent_mi)
        else:
            print("WARNING:  Parent object has invalid asset type "+parent_obj.asset_type+" for MI " + mi_obj.asset_name)
    else:
        print("WARNING:  No parent set for MI " + mi_obj.asset_name)

    data_dict = mi_obj.data_dict
    print("data_dict=")
    print(data_dict)

    if "PhysMaterial" in data_dict:
        print("Found PhysMaterial in data_dict")
        obj_type, obj_name = data_dict["PhysMaterial"]["ObjectName"].split("'")[:2]
        # print("Received object with type "+obj_type)
        # print("Received object with name "+obj_name)

        # print(f"Processing texture {obj_name}...")
        obj_path = '/'.join(data_dict["PhysMaterial"]["ObjectPath"].split(".")[0].split('/')[:-1])

        print('Phys Material path is ' + obj_path)
        print('Phys Material name is ' + obj_name)
        print('Phys Material type is ' + obj_type)

        my_phys_mat = try_create_asset(obj_path, obj_name, obj_type)
        #my_mi.set_editor_property('override_subsurface_profile',True)
        print("Setting Phys Mat to "+my_phys_mat.get_full_name())
        my_mi.set_editor_property('phys_material', my_phys_mat)
        # my_mi.set_editor_property('subsurface_profile', my_ssp)

        #my_mi.get_editor_property('base_property_overrides').set_editor_property('shading_model',
        #                                                                         unreal.MaterialShadingModel.MSM_SUBSURFACE_PROFILE) # TODO:  is this always correct if SubsurfaceProfile is in the JSON ?



    if "SubsurfaceProfile" in data_dict:
        print("Found SubsurfaceProfile in data_dict")
        obj_type, obj_name = data_dict["SubsurfaceProfile"]["ObjectName"].split("'")[:2]
        # print("Received object with type "+obj_type)
        # print("Received object with name "+obj_name)

        # print(f"Processing texture {obj_name}...")
        obj_path = '/'.join(data_dict["SubsurfaceProfile"]["ObjectPath"].split(".")[0].split('/')[:-1])

        print('SSP path is ' + obj_path)
        print('SSP name is ' + obj_name)
        print('SSP type is ' + obj_type)

        my_ssp = try_create_asset(obj_path, obj_name, obj_type)
        #my_mi.set_editor_property('override_subsurface_profile',True)
        print("Setting SubsurfaceProfile to "+my_ssp.get_full_name())
        my_mi.set_editor_property('subsurface_profile', my_ssp)

        #my_mi.get_editor_property('base_property_overrides').set_editor_property('shading_model',
        #                                                                         unreal.MaterialShadingModel.MSM_SUBSURFACE_PROFILE) # TODO:  is this always correct if SubsurfaceProfile is in the JSON ?

    # set ScalarParameterValues
    for key in data_dict['ScalarParameterValues']:
        if 'ParameterValue' in data_dict['ScalarParameterValues'][key]:
            material_util.set_material_instance_scalar_parameter_value(my_mi, key, data_dict['ScalarParameterValues'][key]['ParameterValue'])
            print("Set ScalarParameterValue " + key + "="+str(data_dict['ScalarParameterValues'][key]['ParameterValue']))
        else:
            print("WARNING:  Scalar Parameter Value for "+key+" not found in MI " + mi_obj.asset_name)

    # set VectorParameterValues
    for key in data_dict['VectorParameterValues']:
        if 'ParameterValue' in data_dict['VectorParameterValues'][key]:
            dict_with_rgba = data_dict['VectorParameterValues'][key]['ParameterValue']
            material_util.set_material_instance_vector_parameter_value(my_mi, key, unreal.LinearColor(r=dict_with_rgba['R'], g=dict_with_rgba['G'], b=dict_with_rgba['B'], a=dict_with_rgba['A']))
            print("Set VectorParameterValue "+key+"=")
            print(dict_with_rgba)
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
                windows_texture_path = (texture_root + ('\\').join(obj_path.split('/'))).split('.')[0] + '.tga'

                #print(f"Path={obj_path}")
                #print(f"windows_texture_path={windows_texture_path}")

                full_path = obj_path.split(".")[0] + "." + obj_name
                asset = unreal.load_asset(f"{obj_type}'{full_path}'")

                if asset is None:
                    folder = "/".join(obj_path.split(".")[0].split("/")[:-1])
                    if (Path(windows_texture_path).is_file()):
                        #print("Importing texture at " + windows_texture_path)
                        my_task = buildImportTask(windows_texture_path, folder)
                        tasks = [my_task]
                        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
                        asset = unreal.load_asset(f"{obj_type}'{full_path}'")
                    else:
                        asset = try_create_asset(folder, obj_name, obj_type)
                    #print(asset)
                    if asset is not None:
                        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

                # slot_name = p["ParameterInfo"]["Name"]

                #print(f"Adding texture {full_path} to slot {slot_name}")

                material_util.set_material_instance_texture_parameter_value(my_mi, key , asset)
                print(
                    "Set TextureParameterValue " + key + "=" + asset.get_full_name())
            else:
                print("WARNING:  Texture Parameter Value for "+key+" not found in MI " + mi_obj.asset_name)



    unreal.EditorAssetLibrary.save_loaded_asset(my_mi, False)
    return

# recursively create all material instances in UE, creating parents before children
def recursively_create_material_instances(mi_obj, texture_root=''):

    # create instance for parent
    create_ue_material_instance(mi_obj)
    # recursively create instances for children
    for child_name in mi_obj.children:
        recursively_create_material_instances(mi_obj.children[child_name], texture_root='')
    return