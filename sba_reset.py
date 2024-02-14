import unreal

def main(json_path):
    print("=== RESET SBA ===")
    sel_asset = unreal.EditorUtilityLibrary.get_selected_assets()

    for asset in sel_asset:
        squeeze_bone_data_array = asset.get_editor_property('squeeze_bone_data_array')

        my_dict = {}

        for key in squeeze_bone_data_array:
            #print("Key = "+key)
            #current_bone = squeeze_bone_data_array[key] #.__getitem__(key)
            #print(current_bone)
            my_dict[str(key)] = unreal.SqueezeBoneData() #my_struct

        asset.set_editor_property('squeeze_bone_data_array', my_dict)
        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)