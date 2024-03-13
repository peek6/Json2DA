# Generic script to set up Tekken 8 Item Prefab (IP) assets for various outfit slots from sets of {bi,bci,ci} templates for each part type.

# Author: peek6

# Usage:
#  - Modify the specified part of the script below as described in the comments, then run the script from inside UE.
#  - After packaging, modify the rename_outfit_selector_packages.py script as needed and run it as a regular Python script

# TODO:  So far, I have only used this for the women, Alisa, and women's outfits for Leo.
#  Making mods for men (including men's outfits for Leo) may need some more adjustments to the script.
#  At a minimum, the men's outfits need to be added to the tekken8_parts_and_chars dictionaries, and new ranges of chunk IDs need to be specified for the men's outfit parts

import json

from tekken8_parts_and_chars import chars_dict, body_parts_dict, char_type_letter_dict

# My scripts will be using the 600s and 700s for clothing, and the 800s for skin and hair.
from tekken8_chunk_id_assignments import chunk_id_bases

import unreal
import utils
import importlib
import MaterialExpressions
import materialutil
importlib.reload(utils)
importlib.reload(MaterialExpressions)
importlib.reload(materialutil)
from utils import apply, try_create_asset, create_generic_asset, does_asset_exist, write_assets_to_chunk

from materialutil import buildImportTask

assetTools = unreal.AssetToolsHelpers.get_asset_tools()
assetImportData = unreal.AutomatedAssetImportData()



####################################################################################################################

# SPECIFY ALL PARAMETERS BELOW BEFORE RUNNING SCRIPT.  SCRIPT WILL THEN AUTOMATE EVERYTHING ELSE

mod_name = 'your_mod_name'

print("Generating IP assets and chunks for mod "+mod_name)

# TODO: Set this to root of Content in Fmodel JSON extraction folder
export_root = r"D:\modding\T8_Demo\Exports\Polaris"

ip_asset_path_root = 'Character/Item/Item_Prefab'

texture_path_root = r"D:\modding\T8_Demo\Exports\Polaris\Content\UI\Rep_Texture\CUS_CH_Item"

texture_asset_path_root = 'UI/Rep_Texture/CUS_CH_Item'

# which types of body parts is your mod going on?  Options are shirts, skirts, pants, coats.
body_parts = ['shirts', 'skirts', 'pants']

# which types of chars is your mod going on?  Options are women, men, alisa, leo, other.
chars_types_to_mod = ['women', 'alisa', 'leo']

# Set to True to enable generation of Alisa uppers.  You'll need to add dedicated Alisa meshes and BIs, and point her IPs to them.
enable_alisa_uppers = False

# Components for IPs for each upper part
bi_top = '/Game/Mods/your_mod_name/BI_Mods_your_mod_name_bi_top.BI_Mods_your_mod_name_bi_top'
bci_top = '/Game/Mods/BCI_empty_for_mods.BCI_empty_for_mods'
ci_top = '/Game/Mods/your_mod_name/CI_Mods_your_mod_name_ci_top.CI_Mods_your_mod_name_ci_top'

# Thumbnail texture location for each top part
texture_top = r"D:\modding\T8_Demo\Exports\Polaris\Content\UI\Rep_Texture\CUS_CH_Item\thumbnail_for_top_parts.tga"

# Components for IPs for each bottom part
bi_bottom = '/Game/Mods/your_mod_name/BI_Mods_your_mod_name_bi_bottom.BI_Mods_your_mod_name_bi_bottom'
bci_bottom = '/Game/Mods/BCI_empty_for_mods.BCI_empty_for_mods'
ci_bottom = '/Game/Mods/your_mod_name/CI_Mods_your_mod_name_ci_bottom.CI_Mods_your_mod_name_ci_bottom'

# Thumbnail texture location for each bottom part
texture_bottom = r"D:\modding\T8_Demo\Exports\Polaris\Content\UI\Rep_Texture\CUS_CH_Item\thumbnail_for_bottom_parts.tga"

# Now manually put the mod itself (e.g., all your modded CI, BI, BCI, SK, MI, T, etc.) into a chunk that is not in 600-900.
# My scripts will be using the 600s and 700s for clothing, and the 800s for skin and hair.

# END OF STUFF YOU NEED TO SPECIFY.  SCRIPT SHOULD AUTOMATE EVERYTHING ELSE FOR YOU IF YOU ARE WORKING WITH UPPER AND LOWER CLOTHING PARTS.

####################################################################################################################




# mi_asset_path_root = 'Character/Item/model/unique'

# use chunks 850-860, 850 = all ladies


swap_map = {}
for char_type in chars_types_to_mod:
    for my_char in chars_dict[char_type]:
        swap_map[my_char] = {}
        for body_part in body_parts:
            swap_map[my_char][body_part] = {}
            for my_part in body_parts_dict[body_part]:
                if body_part == 'coats' or body_part=='shirts':
                    if enable_alisa_uppers or (my_char is not 'mnt'):
                        swap_map[my_char][body_part][my_part] =  (bi_top, bci_top, ci_top, texture_top)
                if body_part == 'pants' or body_part=='skirts':
                    swap_map[my_char][body_part][my_part] = (bi_bottom, bci_bottom, ci_bottom, texture_bottom)




# bi_kal_common_skin = unreal.load_asset(bi_top)
empty_bci = unreal.load_asset(bci_bottom)

asset_lists = {}
for body_part in body_parts:
    chunk_id_base = chunk_id_bases[body_part]
    #asset_lists[chunk_id_base] = []
    #asset_lists[chunk_id_base].append(empty_bci)
    body_part_count = 0
    for my_body_part in body_parts_dict[body_part]:
        chunk_id = chunk_id_base + body_part_count
        asset_lists[chunk_id] = []
        asset_lists[chunk_id].append(empty_bci)
        body_part_count = body_part_count + 1


t8_target_body_parts = {
    'coats':'bdu',
    'shirts':'bdu',
    'skirts':'btm',
    'pants':'btm'
}


for char_type in chars_types_to_mod:
    char_type_letter = char_type_letter_dict[char_type]
    for target_char in chars_dict[char_type]:
        for target_body_part in swap_map[target_char]:
            body_part_count = 0
            chunk_id_base = chunk_id_bases[target_body_part]
            t8_target_body_part = t8_target_body_parts[target_body_part]
            for target_part in swap_map[target_char][target_body_part]:


                if target_body_part == 'coats' or target_body_part == 'shirts':
                    t8_target_body_part = 'bdu'

                if target_body_part == 'skirts' or target_body_part == 'pants':
                    t8_target_body_part = 'btm'


                (bi,bci,ci,texture_file) = swap_map[target_char][target_body_part][target_part]

                # if target_char != source_char:
                # load the JSON for the swap_map[char][key]
                #json_path = export_root +'/Content/'+ip_asset_path_root+'/'+char+'/'+body_part+'/IP_'+char+'_'+body_part+'_'+swap_map[char][body_part][key]+'.json'
                # json_path = export_root + '/Content/' + ip_asset_path_root + '/' + source_char + '/' + source_body_part+'/'+'IP_'+ source_char+'_'+source_body_part+'_'+source_part+'.json'


                # load it into the IP for key
                asset_path = '/Game/'+ip_asset_path_root+'/'+target_char+'/'+t8_target_body_part+'/'
                asset_name = 'IP_'+target_char+'_'+t8_target_body_part+char_type_letter+target_part

                # print("Loading JSON "+json_path)
                print("Writing to asset {"+asset_path+', '+asset_name+'}')

                #with open(json_path, "r+") as fp:
                #    data = json.load(fp)[0]["Properties"]

                #OVERWRITE_EXISTING = True

                if unreal.EditorAssetLibrary.does_asset_exist(asset_path+asset_name): # does_asset_exist(asset_path, asset_name):
                    asset = unreal.load_asset(asset_path + asset_name) # + '.' + asset_name)
                    unreal.EditorAssetLibrary.delete_loaded_asset(asset) # asset_path + asset_name)

                clazz = unreal.ItemPrefab
                factory = unreal.ItemPrefabFactory
                asset = try_create_asset(asset_path, asset_name, "ItemPrefab")

                #apply(asset, data) # asset_data)

                #empty_bci = unreal.load_asset('/Game/Mods/BCI_empty_for_mods.BCI_empty_for_mods')

                bi_asset = unreal.load_asset(bi)
                bci_asset = unreal.load_asset(bci)
                ci_asset = unreal.load_asset(ci)

                asset.set_editor_property('base_character_item_ref', bci_asset)
                asset.set_editor_property('customize_item_ref', ci_asset)
                asset.set_editor_property('base_item_ref', bi_asset)

                unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

                chunk_id = chunk_id_base + body_part_count

                # asset_lists[chunk_id_base].append(asset)
                asset_lists[chunk_id].append(asset)

                # swap thumbnails
                new_texture_path = texture_file # texture_path_root + '\\' + source_char + '\\T_UI_CUS_CH_item_' + source_char + '_' + source_body_part + '_' + source_part + '.png'
                original_loaded_asset_name = new_texture_path.split('\\')[-1].split('.')[0]

                # load it into the texture for key
                asset_path = '/Game/' + texture_asset_path_root + '/' + target_char + '/'
                #original_loaded_asset_name = 'T_UI_CUS_CH_item_' + source_char + '_' + source_body_part + '_' + source_part #  + char + '_' + body_part + '_' + swap_map[char][body_part][key]
                desired_new_asset_name = 'T_UI_CUS_CH_item_' + target_char + '_' + t8_target_body_part + char_type_letter + target_part

                if unreal.EditorAssetLibrary.does_asset_exist(asset_path+desired_new_asset_name): # does_asset_exist(asset_path, asset_name):
                    asset = unreal.load_asset(asset_path+desired_new_asset_name) # + '.' + asset_name)
                    unreal.EditorAssetLibrary.delete_loaded_asset(asset) # asset_path + asset_name)


                # print("Loading texture " + new_texture_path)
                # print("To asset {" + asset_path + ', ' + asset_name + '}')

                tasks = [buildImportTask(new_texture_path, asset_path)]
                assetTools.import_asset_tasks(tasks)

                asset = unreal.load_asset(asset_path + original_loaded_asset_name + '.' + original_loaded_asset_name)
                asset.set_editor_property('never_stream', True)
                unreal.EditorAssetLibrary.save_loaded_asset(asset, False)
                unreal.EditorAssetLibrary.rename_loaded_asset(asset,
                                                              asset_path + desired_new_asset_name + '.' + desired_new_asset_name)

                chunk_id = chunk_id_base + body_part_count

                # asset_lists[chunk_id_base].append(asset)
                asset_lists[chunk_id].append(asset)

                body_part_count = body_part_count+1

for body_part in body_parts:
    chunk_id_base = chunk_id_bases[body_part]
    #write_assets_to_chunk('/Game/chunks', 'chunk' + str(chunk_id_base) + '_for_all_' + body_part, chunk_id_base,
    #                      asset_lists[chunk_id_base])
    body_part_count = 0
    for my_body_part in body_parts_dict[body_part]:
        chunk_id = chunk_id_base + body_part_count
        write_assets_to_chunk('/Game/chunks', 'chunk' + str(chunk_id) + '_' + my_body_part,
                              chunk_id,
                              asset_lists[chunk_id])
        body_part_count = body_part_count + 1