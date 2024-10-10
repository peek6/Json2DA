import unreal

assets_to_set = [
#'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_dogi_damage_sho_f_heellongboots_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_dogi_damage_sho_f_kunoichi_shoes_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenimdamage_sho_f_kunoichi_shoes_in',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenim_sho_f_canvassneaker',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenim_sho_f_furshortboots_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenim_sho_f_heellongboots_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenim_sho_f_kunoichi_shoes_in',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenim_sho_f_prowrestling',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenim_sho_f_running',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenim_sho_f_sandals',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenim_sho_f_sneakers',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_mdenim_sho_f_tropical',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_ankleprotector',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_canvassneaker',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_heellongboots',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_highheal',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_kunoichi_shoes',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_laceup',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_loaferA',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_officemule',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_running',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_sandals',
# '/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_prowrestling_sho_f_straighttip',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_slacks_sho_f_furshortboots_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_slacks_sho_f_heellongboots_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_slacks_sho_f_kunoichi_shoes_in',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_slacks_sho_f_prowrestling',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_slacks_sho_f_sneakers',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_slacks_sho_f_tropical',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_tracksuit_sho_f_furshortboots_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_tracksuit_sho_f_heellongboots_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_tracksuit_sho_f_kunoichi_shoes_in',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_tracksuit_sho_f_prowrestling',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_tracksuit_sho_f_running',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_tracksuit_sho_f_sneakers',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_tracksuit_sho_f_tracksuit',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_tracksuit_sho_f_tropical',
'/Game/Character/Item/Squeeze_Bone_Asset/cf0/btm/SBA_f_widepants_denim_sho_f_prowrestling',
'/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_f_mdenimdamage_sho_f_tropical',
'/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_f_slacksseven_check_sho_f_prowrestling',
'/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_f_slacks_sho_f_prowrestling',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_cargo_sho_f_prowrestling',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_easy_sho_f_prowresling',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_easy_sho_f_trackshoes',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_easy_sho_f_tropical',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_endbiker_sho_f_canvassneaker',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_endbiker_sho_f_trachsuit',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_ninja_lower_sho_f_prowrestling',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_slacks_sho_f_ankleprotector',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_slacks_sho_f_running',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_slacks_sho_f_sneakers',
# '/Game/Character/Item/Squeeze_Bone_Asset/ghp/btm/SBA_ghp_m_slacks_sho_f_tropical',
#'/Game/Character/Item/Squeeze_Bone_Asset/mnt/btm/SBA_mnt_f_mdenimdamage_sho_f_kunoichi_shoes_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/mnt/btm/SBA_mnt_f_mdenim_sho_f_kunoichi_shoes_in',
#'/Game/Character/Item/Squeeze_Bone_Asset/mnt/btm/SBA_mnt_f_slacks_sho_f_kunoichi_shoes_in',
'/Game/Character/Item/Squeeze_Bone_Asset/mnt/btm/SBA_mnt_f_tracksuit_sho_f_furshortboots_in'
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