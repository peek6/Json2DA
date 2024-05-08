import unreal
import map_types
import importlib
importlib.reload(map_types)
from map_types import MAP_TYPES, FACTORY_MAP, ARRAY_TYPES

material_util = unreal.MaterialEditingLibrary()

def get_factory_from_class(clazz):
    for c in clazz.__mro__:
        if c.__name__ in FACTORY_MAP and len(FACTORY_MAP[c.__name__]) > 0: return FACTORY_MAP[c.__name__]

def create_with_factory(folder, name, clazz, factory_name):
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = getattr(unreal, factory_name)()
    print(factory)
    return tools.create_asset(name, folder, clazz, factory)

def create_generic_asset(folder, name, clazz, factory_name): # (asset_path='', unique_name=True, asset_class=None, asset_factory=None):
    #if unique_name:
    #    asset_path, asset_name = unreal.AssetToolsHelpers.get_asset_tools().create_unique_asset_name(base_package_name=asset_path, suffix='')
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path=folder+'/'+name): # asset_path):
        #path = asset_path.rsplit('/', 1)[0]
        #name = asset_path.rsplit('/', 1)[1]
        return unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=name, package_path=folder, asset_class=clazz, factory=factory_name)
    return unreal.load_asset(folder+'/'+name)


def write_assets_to_chunk(chunk_asset_path, chunk_asset_name, chunk_id, list_of_assets):

    if chunk_asset_path[-1]=='/':
        full_chunk_path = chunk_asset_path+chunk_asset_name
        chunk_asset_path_slash = chunk_asset_path
    else:
        full_chunk_path = chunk_asset_path + '/' + chunk_asset_name
        chunk_asset_path_slash = chunk_asset_path + '/'

    if unreal.EditorAssetLibrary.does_asset_exist(asset_path=full_chunk_path):
        chunk_asset = unreal.load_asset(full_chunk_path)
    else:
        chunk_asset = unreal.PrimaryAssetLabel()
        unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(chunk_asset_name, chunk_asset_path_slash, chunk_asset)
        unreal.EditorAssetLibrary.save_asset(full_chunk_path)
        chunk_asset = unreal.load_asset(full_chunk_path)

    chunk_asset.set_editor_property('explicit_assets', list_of_assets)
    chunk_asset.get_editor_property('rules').set_editor_property('chunk_id', chunk_id)
    unreal.EditorAssetLibrary.save_loaded_asset(chunk_asset, False)

def try_create_asset(folder, name, type_str):

    if folder[-1]=='/':
        full_path = folder+name
    else:
        full_path = folder + '/' + name

    if unreal.EditorAssetLibrary.does_asset_exist(asset_path=full_path):  #folder + '/' + name):
        return unreal.load_asset(full_path) # folder + '/' + name)

    if not hasattr(unreal, type_str):
        unreal.log_error(f"{type_str} does not exist")
        return
    
    clazz = getattr(unreal, type_str)
    available_factories = get_factory_from_class(clazz)

    if available_factories is None:
        unreal.log_error(f"{type_str} does not have a factory")
        return

    for factory_name in available_factories:
        print(f"Trying {factory_name}")
        try:
            asset =  create_with_factory(folder, name, clazz, factory_name)
            if asset is not None: return asset
        except Exception as e: unreal.log_error(e)

    return None

def as_key_pair(data):
    return [list(x.items())[0] for x in data]

def does_asset_exist(folder, name):
    return unreal.EditorAssetLibrary.does_asset_exist(folder + "/" + name)

def create_linked_asset(data):
    print("Data is "+str(data))
    obj_type, obj_name = data["ObjectName"].split("'")[:2]
    full_path = data["ObjectPath"].split(".")[0] + "." + obj_name
    asset = unreal.load_asset(f"{obj_type}'{full_path}'")

    if asset is None:
        folder = "/".join(data["ObjectPath"].split(".")[0].split("/")[:-1])
        asset = try_create_asset(folder, obj_name, obj_type)
        print(asset)
        if asset is not None: unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

    return asset

def create_recursive_linked_asset(obj_type_arg, data):

    #obj_type, obj_name = data["AssetPathName"].split("'")[:2]
    #full_path = data["ObjectPath"].split(".")[0] + "." + obj_name
    #asset = unreal.load_asset(f"{obj_type}'{full_path}'")

    if data["AssetPathName"]=="None":
        return None
    else:
        obj_type = obj_type_arg
        folder = "/".join(data["AssetPathName"].split(".")[0].split("/")[:-1])
        obj_name = data["AssetPathName"].split(".")[0].split("/")[-1]
        full_path = data["AssetPathName"]

        print(f"Creating recursive linked asset {full_path}")
        print(f"Using folder={folder}, obj_name={obj_name}, obj_type={obj_type}")

        asset = unreal.load_asset(f"{full_path}")


        if asset is None:
            asset = try_create_asset(folder, obj_name, obj_type)
            print(asset)
            if asset is not None: unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

        return asset

def get_typestr_from_name(name : str):
    return name.split("'")[0]

# EGearSlotIDEnum::BACK => GearSlotIDEnum.BACK
def str_to_enum(val):
    enum_type, enum_val = val.split("::")
    enum_type = enum_type[1:]
    if enum_type == 'MaterialShadingModel' and enum_val=='MSM_SubsurfaceProfile':
        return unreal.MaterialShadingModel.MSM_SUBSURFACE_PROFILE
    else:
        return getattr(getattr(unreal, enum_type), enum_val)

def try_get_map_value_type(map_obj, key):
    try:
        map_obj[key] = {}
    except:
        try:
            map_obj[key] = 0
        except:
            pass
        pass
    
    try:
        if map_obj.get(key) is None: return None

        ty = type(map_obj.pop(key))
        return ty.__name__
    except:
        return None

def try_get_map_type(obj, key):
    map_obj = obj.get_editor_property(key)
    if key in MAP_TYPES:
        return MAP_TYPES[key]

    print("ERROR:  Did not find key "+str(key)+" in MAP_TYPES")
    
    try:
        map_obj["_"] = {}
    except:
        try:
            map_obj["_"] = 0
        except:
            pass
        pass
    
    try:
        if map_obj.get("_") is None: return None

        ty = type(map_obj.pop("_"))
        return { "Key": "str", "Value": ty.__name__ }
    except:
        return None


def try_get_array_type(obj, key):
    map_obj = obj.get_editor_property(key)
    if key in ARRAY_TYPES:
        print("Found key "+str(key)+" in ARRAY_TYPES")
        return ARRAY_TYPES[key]
    print("ERROR:  Did not find key "+str(key)+" in ARRAY_TYPES")
    return None

    
def update_map(m_prop, data, ty):
    v_ty = ty["Value"]
    k_ty = ty["Key"]
    
    if k_ty == "": k_ty = "str"


    is_builtin = v_ty in __builtins__

    print("Setting up map of type " + k_ty)
    
    for key, value in as_key_pair(data):

        print("k_ty is "+str(k_ty))
        print("key is "+str(key))
        print("value is "+str(value))

        if k_ty != "str" and unreal.EnumBase in getattr(unreal, k_ty).__mro__:
            key = str_to_enum(key)

        if v_ty == "":
            v_ty = try_get_map_value_type(m_prop, key)
            if v_ty is None: print(key)
        if v_ty == "__AssetRef":
            uvalue =  create_linked_asset(value)
        if v_ty == 'Assign_Surface_Preset':
            my_asset = unreal.SurfacePreset()
            apply(my_asset, value)
            uvalue = my_asset
        if v_ty == 'Assign_Surface_Data':
            my_asset = unreal.SurfaceData()
            apply(my_asset, value)
            uvalue = my_asset
        else:
            uvalue = value if is_builtin else  getattr(unreal, v_ty)()
            if not is_builtin: apply(uvalue, value)
    
       
        m_prop[key] = uvalue

    return m_prop


def update_array(m_prop, data, ty):
    v_ty = ty["Value"]
    #k_ty = ty["Key"]
    
    #if k_ty == "": k_ty = "str"

    is_builtin = v_ty in __builtins__

    # clear the array. why doesn't the api have a clear function?
    original_size = len(m_prop) 
    for idx in range(original_size):
        m_prop.pop()
    
    #for key, value in as_key_pair(data):
    # resize to the correct length.   I need to do it this way since the resize function seems to be broken.
    #for value_idx in range(len(data)):
    #    m_prop.append("1")

    new_size = len(data)
    print("Setting up array of size "+str(new_size))
    for value_idx in range(new_size):
        value = data[value_idx]
        #if k_ty != "str" and unreal.EnumBase in getattr(unreal, k_ty).__mro__:
        #    key = str_to_enum(key)

        #if v_ty == "":
        #    v_ty = try_get_map_value_type(m_prop, key)
        #    if v_ty is None: print(key)
        print("v_ty is "+str(v_ty))
        print("value is "+str(value))
        if v_ty == "__AssetRef" and "ObjectName" in value:
            uvalue =  create_linked_asset(value)
            #elif v_ty == 'OverrideMaterials':
            #    uvalue = create_linked_asset(value)
        elif v_ty == 'ItemPrefab':
            uvalue = create_recursive_linked_asset(v_ty, value)
            #my_struct = unreal.DesignAssignStruct()
            #apply(my_struct, value)
            # for  in data:
            #    set_editor_property(my_struct, key,data[key])
            # asset = unreal.CustomizeItem()
            # apply(asset, data)
            #my_folder
            #uvalue = try_create_asset(my_folder, my_name, 'ItemPrefab')# my_struct
        elif v_ty == 'PhoenixDynamicBoneBinariesItem':
            my_struct = unreal.DynamicBoneDataStruct() # Array(unreal.PhoenixDynamicBoneBinary) # unreal.DesignAssignStruct()
            apply(my_struct,value)
            uvalue = my_struct

            '''
            temp = create_linked_asset(value["Data"])
            my_array.insert(0, temp)
            #apply(my_array, value)
            uvalue = my_array
            set_editor_property(asset, key, data[key])
            # uvalue = create_linked_asset(value["Data"])
            # apply(uvalue, value)
            #uvalue = value if is_builtin else  getattr(unreal, v_ty)()
            #if not is_builtin: apply(uvalue, value)
            '''

        elif v_ty == 'RawData':
            uvalue = value
        elif v_ty == 'Capsules':
            # TODO:  Create a struct here
            my_struct = unreal.ImportCapsuleCollisionVolume()
            apply(my_struct, value)
            #for  in data:
            #    set_editor_property(my_struct, key,data[key])
            # asset = unreal.CustomizeItem()
            # apply(asset, data)
            uvalue = my_struct
        elif v_ty == 'DesignAssignSlotArray':
            # TODO:  Create a struct here
            my_struct = unreal.DesignAssignStruct()
            apply(my_struct, value)
            uvalue = my_struct
        elif v_ty == 'AssignPerMaterialArray':
            # TODO:  Create a struct here
            my_struct = unreal.AssignPerMaterialStruct()
            apply(my_struct, value)
            uvalue = my_struct
        elif v_ty == 'DesignAssignArray':
            # TODO:  Create a struct here
            my_struct = unreal.DesignAssignStruct()
            apply(my_struct, value)
            uvalue = my_struct
        elif v_ty == 'EyeParamArray':
            # TODO:  Create a struct here
            my_struct = unreal.BaseEyeItemOneEye()
            apply(my_struct, value)
            uvalue = my_struct
        else:
            uvalue = value if is_builtin else  getattr(unreal, v_ty)()
            if not is_builtin: apply(uvalue, value)
    
       
        m_prop.insert(value_idx, uvalue)

    return m_prop


# Like obj.set_editor_property except it takes our JSON as a value
def set_editor_property(obj, key, value):
    try:
        prop = obj.get_editor_property(key)
    except:
        return
    ty = type(prop)
    print("Running set_editor_property on type " + str(ty) + " with key "+str(key)) #+" and value "+str(value))


    #print("Processing key: ")
    #print(key)
    #print("Type: ")
    #print(ty)

    if ty in (unreal.Name, str, float, bool, int):
        print("peek:  Found primitive for key "+ key)
        obj.set_editor_property(key, value)
    elif unreal.EnumBase in ty.__mro__:
        print("peek:  Found enum for key "+ key)
        obj.set_editor_property(key, str_to_enum(value))
    elif ty is unreal.Map:
        print("peek:  Found map for key "+ key)
        if len(value) > 0:
            map_ty = try_get_map_type(obj, key)
            if map_ty is None: 
                unreal.log_error(f"Map {key} is unknown, leaving blank")
            else:
                obj.set_editor_property(key, update_map(prop, value, map_ty))
    elif isinstance(value, dict) and "ObjectName" in value:
        print("peek:  Found linked asset for key "+ key)
        if type(obj)==unreal.MaterialInstanceConstant and key=='SubsurfaceProfile':
            print("Found SubsurfaceProfile in MI JSON")
            obj_type, obj_name = value["ObjectName"].split("'")[:2]
            # print("Received object with type "+obj_type)
            # print("Received object with name "+obj_name)

            # print(f"Processing texture {obj_name}...")
            obj_path = '/'.join(value["ObjectPath"].split(".")[0].split('/')[:-1])

            print('SSP path is ' + obj_path)
            print('SSP name is ' + obj_name)
            print('SSP type is ' + obj_type)

            my_ssp = try_create_asset(obj_path, obj_name, obj_type)
            obj.set_editor_property('override_subsurface_profile', True)
            print("Setting SubsurfaceProfile to " + my_ssp.get_full_name())
            obj.set_editor_property('subsurface_profile', my_ssp)

            obj.get_editor_property('base_property_overrides').set_editor_property('shading_model',
                                                                                     unreal.MaterialShadingModel.MSM_SUBSURFACE_PROFILE)  # TODO:  is this always correct if SubsurfaceProfile is in the JSON ?
        else:
            obj.set_editor_property(key, create_linked_asset(value))
    elif isinstance(value, dict) and "AssetPathName" in value:
        print("Found a recursive asset pointer for key "+ key)
        obj.set_editor_property(key, create_recursive_linked_asset(key, value))
    elif unreal.StructBase in ty.__mro__:
        print("peek:  Found struct for key "+ key)
        apply(prop, value)
    elif ty is unreal.Array: #y.__name__ in 'Array':
        print("peek:  Found array of length "+str(len(value)) + " for key "+ key)
        if len(value) > 0:
            array_ty = try_get_array_type(obj, key)
            print("prop is"+str(prop))
            print("value is"+str(value))
            print("array_ty is"+str(array_ty))
            if type(obj)==unreal.MaterialInstanceConstant and array_ty['Value'] == 'TextureParameterValues':
                mi_apply_texture_parameters(obj, value)
                # mi_apply_texture_parameter(uvalue, value)
                # uvalue = create_linked_asset(value)
            elif type(obj)==unreal.MaterialInstanceConstant and array_ty['Value'] == 'ScalarParameterValues':
                mi_apply_scalar_parameters(obj, value)
            elif type(obj)==unreal.MaterialInstanceConstant and array_ty['Value'] == 'VectorParameterValues':
                mi_apply_texture_parameters(obj, value)
            else:
                obj.set_editor_property(key, update_array(prop, value, array_ty))
        #for array_idx in range(len(value)):
        #    prop.append('1') #create_array_elem_property(obj,key,value[array_idx])) #'0')
        #    temp = create_array_elem_property(obj,key,value[array_idx]) #key+'['+str(array_idx)+']',value[array_idx])
        #    #print(temp)
        #    prop.insert(array_idx, temp)
    else:
        print(f"WARNING:  Unknown Type {ty.__name__} for key {key} with value {value}")
    

def apply(asset, data : dict):
    print("Running apply on asset "+str(asset)) # +" with data "+str(data)+" with type "+str())
    for key in data:
        set_editor_property(asset, key, data[key])
    
def mi_apply_scalar_parameters(my_mi, data_array):
    for data in data_array:
        print("Running mi_apply_scalar_parameter on parameter with name "+data["ParameterInfo"]["Name"]+" and value "+str(data["ParameterValue"]))
        material_util.set_material_instance_scalar_parameter_value(my_mi, data["ParameterInfo"]["Name"], data['ParameterValue'])
def mi_apply_vector_parameters(my_mi, data_array):
    for data in data_array:
        dict_with_rgba = data['ParameterValue']
        print("Running mi_apply_vector_parameter on parameter with name " + data["ParameterInfo"][
            "Name"] + " and value " + str(data["ParameterValue"]))
        material_util.set_material_instance_vector_parameter_value(my_mi,
                                                                   data["ParameterInfo"]["Name"],
                                                                   unreal.LinearColor(
                                                                        r=dict_with_rgba['R'],
                                                                        g=dict_with_rgba['G'],
                                                                        b=dict_with_rgba['B'],
                                                                        a=dict_with_rgba['A']
                                                                   )
                                                                   )
    # print("Running mi_apply_vector_parameter on asset "+str(my_mi)) # +" with data "+str(data)+" with type "+str())

def mi_apply_texture_parameters(my_mi, p_array):
    for p in p_array:
        key = p["ParameterInfo"]["Name"]
        if 'ParameterValue' in p:
            if not (p["ParameterValue"] is None):
                obj_type, obj_name = p["ParameterValue"]["ObjectName"].split("'")[:2]
                # print("Received object with type "+obj_type)
                # print("Received object with name "+obj_name)

                #print(f"Processing texture {obj_name}...")
                obj_path = p["ParameterValue"]["ObjectPath"]
                # windows_texture_path = (texture_root + ('\\').join(obj_path.split('/'))).split('.')[0] + '.tga'

                #print(f"Path={obj_path}")
                #print(f"windows_texture_path={windows_texture_path}")

                full_path = obj_path.split(".")[0] + "." + obj_name
                asset = unreal.load_asset(f"{obj_type}'{full_path}'")

                if asset is None:
                    folder = "/".join(obj_path.split(".")[0].split("/")[:-1])
                    asset = try_create_asset(folder, obj_name, obj_type)

                if asset is not None:
                    unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

                # slot_name = p["ParameterInfo"]["Name"]

                #print(f"Adding texture {full_path} to slot {slot_name}")

                material_util.set_material_instance_texture_parameter_value(my_mi, key , asset)

