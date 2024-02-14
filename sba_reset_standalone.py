import unreal

assets_to_set = [
    '/Game/Character/Item/Base_Character_Item/cf0/btm/SBA_f_mdenim_sho_f_sandals'
]

for my_asset_name in assets_to_set:

    asset = unreal.EditorAssetLibrary.load_asset(my_asset_name)

    squeeze_bone_data_array = asset.get_editor_property('squeeze_bone_data_array')

    my_dict = {}

    for key in squeeze_bone_data_array:

        print("Key = "+key)
        current_bone = squeeze_bone_data_array[key] #.__getitem__(key)
        print(current_bone)
        #print('Location = '+current_bone.__getitem__('Location'))
        #print('Rotation = ' + squeeze_bone_data_array[str(key)]['Rotation'])
        #print('Scale = ' + squeeze_bone_data_array[str(key)]['Scale'])
        #struct my_struct
        #my_struct.transform.rotation.x = 0
        my_dict[str(key)] = unreal.SqueezeBoneData() #my_struct

    asset.set_editor_property('squeeze_bone_data_array', my_dict)
    unreal.EditorAssetLibrary.save_asset(my_asset_name)