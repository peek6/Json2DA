# Imports all textures specified in a text file in Content/Python/all_textures.txt
# You can yse create_texture_file.py to create this text file
# You can then use to replace the dummy textures with the real ones.
# all_textures can have all the textures, or just the subset you want to import

# Author:  peek6

# Usage: Generate Content/Python/all_textures.txt,  point the script to your UE project root, and run the script.



from pathlib import Path


import importlib
import unreal
import MaterialExpressions
import materialutil
importlib.reload(MaterialExpressions)
importlib.reload(materialutil)
from materialutil import buildImportTask

assetTools = unreal.AssetToolsHelpers.get_asset_tools()
assetImportData = unreal.AutomatedAssetImportData()

# TODO: Set this to your UE project root
project_root = r"D:\polar_project_custom_git"





count = 0

task_tuples = []

# print("Hello World.")



with open(project_root + '\\' + 'Content\\Python\\all_textures.txt','r') as fp:
    lines = fp.readlines()

for line in lines:
    texture_path_to_import = line.strip()
    tokens = texture_path_to_import.split('\\')
    asset_name = tokens[-1].split('.')[0]
    tokens_after_content = []
    found_content = False
    for token in tokens[:-1]:
        if (token == 'Game'):
            found_content = True
            tokens_after_content.append('Game')
        else:
            if (found_content):
                tokens_after_content.append(token)
    asset_path = '/' + '/'.join(tokens_after_content) + '/'

    asset = unreal.load_asset(asset_path+asset_name+'.'+asset_name)
    unreal.EditorAssetLibrary.delete_loaded_asset(asset)

    tasks = [buildImportTask(texture_path_to_import, asset_path)]
    #assetImportData.destination_path = asset_path
    #assetImportData.filenames = [texture_path_to_import]
    #assetTools.import_assets_automated(assetImportData)
    assetTools.import_asset_tasks(tasks)

    asset = unreal.load_asset(asset_path+asset_name+'.'+asset_name)
    asset.set_editor_property('never_stream', True)
    if(asset_name[-2:]=='_C'):
        asset.set_editor_property('srgb', True)
    else:
        asset.set_editor_property('srgb',False)
    unreal.EditorAssetLibrary.save_loaded_asset(asset, False)
    # print(texture_path_to_import)
    # print(asset_path)
    # print(asset_name)
    count = count+1


