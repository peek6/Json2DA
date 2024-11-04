# Script to batch import all outfit gear DAs from a directory

# Usage:
#  - In DIRECTORY, specify the directory with your outfit gear DA JSON files exported from Fmodel
#  - In OUTPUT_BASE_PATH, specify the UE path to the outfit DA assets
#  - I assume you first delete all your existing DA assets in UE before running this script.  If you want the script to be able to overwrite assets in UE, change OVERWRITE_EXISTING to True.

import unreal
import os
from glob import glob
import json
import importlib
import utils
importlib.reload(utils)
from utils import apply, does_asset_exist, try_create_asset

DIRECTORY = r"D:\games\tools\FModel\Output\Exports\Phoenix\Content\Data\GearAppearances\Outfit\Modded"

DIRECTORY_GLOB = f"{DIRECTORY}\**\DA_*.json"
OVERWRITE_EXISTING = False
OUTPUT_BASE_PATH = "/Game/Data/GearAppearances/Outfit/"  # peek:  for CreatorKit, use /your_mod_name/Data/GearAppearances/Outfit/

SKIP_DIALOG = False

def get_asset_path(filename : str):
    relpath = os.path.relpath(filename, DIRECTORY)
    relpath = os.path.splitext(relpath)[0]
    relpath = OUTPUT_BASE_PATH + "/".join(os.path.normpath(relpath).split(os.sep)[:-1])
    return relpath

def load_asset_from_json(filename : str):
    with open(filename, "r") as fp:
        data = json.load(fp)[0]

    
    asset_type = data["Type"]
    asset_name = data["Name"]
    asset_data = data["Properties"]

    asset_folder = get_asset_path(filename)

    if does_asset_exist(asset_folder, asset_name):
        if OVERWRITE_EXISTING:
            unreal.EditorAssetLibrary.delete_asset(asset_folder + "/" + asset_name)
        else:
            print(f"Skipping {asset_name}")
            return

    asset = try_create_asset(asset_folder, asset_name, asset_type)
    apply(asset, asset_data)
    unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

    

def main():
    global OUTPUT_BASE_PATH
    print(f"Loading dir {DIRECTORY}")
    files = glob(DIRECTORY_GLOB, recursive=True)
    print(f"{len(files)} files found")
    print(f"Overwrite Existing = {OVERWRITE_EXISTING}")

    if not OUTPUT_BASE_PATH.endswith("/"):
        unreal.EditorDialog.show_message(
            "Config Error",
            "OUTPUT_BASE_PATH must end with a '/'",
            unreal.AppMsgType.OK
        )
        return


    if (not SKIP_DIALOG) and unreal.EditorDialog.show_message(
        "JSON2DA Mass Import", 
        "\n".join([
            f"{len(files)} files were found",
            f"Overwrite Existing = {OVERWRITE_EXISTING}",
            f"Import Path = {DIRECTORY}",
            f"Output Path = {OUTPUT_BASE_PATH}",
            f"Files will be imported as <Relative Path to File (from Import Path)>/<Asset Name>",
            "Continue with import?"
        ]),
        unreal.AppMsgType.YES_NO
    ) != unreal.AppReturnType.YES:
        print("Action Cancelled By User")
        return

    with unreal.ScopedSlowTask(len(files), "Loading Files") as slow_task:
        slow_task.make_dialog(True)
        for file in files:
            if slow_task.should_cancel(): return
            try:
                load_asset_from_json(file)
            except Exception as e:
                unreal.log_error(f"{file} Failed to load")
                unreal.log_error(e)

