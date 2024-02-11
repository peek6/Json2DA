import unreal
import map_types
import importlib
importlib.reload(map_types)
from map_types import MAP_TYPES, FACTORY_MAP, ARRAY_TYPES

def get_factory_from_class(clazz):
    for c in clazz.__mro__:
        if c.__name__ in FACTORY_MAP and len(FACTORY_MAP[c.__name__]) > 0: return FACTORY_MAP[c.__name__]

def create_with_factory(folder, name, clazz, factory_name):
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = getattr(unreal, factory_name)()
    print(factory)
    return tools.create_asset(name, folder, clazz, factory)

def try_create_asset(folder, name, type_str):
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
            #for  in data:
            #    set_editor_property(my_struct, key,data[key])
            # asset = unreal.CustomizeItem()
            # apply(asset, data)
            uvalue = my_asset
        if v_ty == 'Assign_Surface_Data':
            my_asset = unreal.SurfaceData()
            apply(my_asset, value)
            #for  in data:
            #    set_editor_property(my_struct, key,data[key])
            # asset = unreal.CustomizeItem()
            # apply(asset, data)
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
        elif v_ty == 'DesignAssignSlotArray':
            # TODO:  Create a struct here
            my_struct = unreal.DesignAssignStruct()
            apply(my_struct, value)
            #for  in data:
            #    set_editor_property(my_struct, key,data[key])
            # asset = unreal.CustomizeItem()
            # apply(asset, data)
            uvalue = my_struct
        elif v_ty == 'AssignPerMaterialArray':
            # TODO:  Create a struct here
            my_struct = unreal.AssignPerMaterialStruct()
            apply(my_struct, value)
            #set_editor_property(my_struct, key,data[key])
            uvalue = my_struct
        elif v_ty == 'DesignAssignArray':
            # TODO:  Create a struct here
            my_struct = unreal.DesignAssignStruct()
            apply(my_struct, value)
            #set_editor_property(my_struct, key,data[key])
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
    print("Running set_editor_property on type " + str(ty))


    #print("Processing key: ")
    #print(key)
    #print("Type: ")
    #print(ty)

    if ty in (unreal.Name, str, float, bool, int):
        obj.set_editor_property(key, value)
    elif unreal.EnumBase in ty.__mro__:
        obj.set_editor_property(key, str_to_enum(value))
    elif ty is unreal.Map:
        if len(value) > 0:
            map_ty = try_get_map_type(obj, key)
            if map_ty is None: 
                unreal.log_error(f"Map {key} is unknown, leaving blank")
            else:
                obj.set_editor_property(key, update_map(prop, value, map_ty))
    elif isinstance(value, dict) and "ObjectName" in value:
        obj.set_editor_property(key, create_linked_asset(value))
    elif isinstance(value, dict) and "AssetPathName" in value:
        print("Found a recursive asset pointer.")
        obj.set_editor_property(key, create_recursive_linked_asset(key, value))
    elif unreal.StructBase in ty.__mro__:
        apply(prop, value)
    elif ty is unreal.Array: #y.__name__ in 'Array':
        print("peek:  Found array of length "+str(len(value)) + " for key "+ key)
        if len(value) > 0:
            array_ty = try_get_array_type(obj, key)
            print("prop is"+str(prop))
            print("value is"+str(value))
            print("array_ty is"+str(array_ty))
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
    
