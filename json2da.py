import json
import io
from contextlib import redirect_stdout

import unreal
import importlib

import utils
importlib.reload(utils)

from utils import apply


def main(json_path):
    print("=== JSON 2 T8 ASSET ===")
    sel_asset = unreal.EditorUtilityLibrary.get_selected_assets()
    with open(json_path.file_path, "r+") as fp:
        temp_buffer = json.load(fp)[0]
        if "Properties" in temp_buffer:
            data = temp_buffer["Properties"]
        else:
            print("Warning:  JSON file has no properties to populate")
            data = {}



        for asset in sel_asset:
            with redirect_stdout(io.StringIO()) as f:
                print(asset)
            s = f.getvalue()
            if ('PhoenixSkeletonBinary' in s) or ('PhoenixDynamicBoneBinary' in s):
                if 'RawData' in data:
                    asset.set_editor_property('RawData', data['RawData'])
                else:
                    print("Warning:  No RawData found for asset "+s)
                if 'Version' in data:
                    asset.set_editor_property('Version', data['Version'])
                else:
                    print("Warning:  No Version found for asset"+s)
            else:
                apply(asset, data)

        # [apply(asset, data) for asset in sel_asset]
        for asset in sel_asset:
            unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

'''
def main(json_string):
    print("=== JSON 2 T8 ASSET ===")
    sel_asset = unreal.EditorUtilityLibrary.get_selected_assets()
    data = json.loads(json_string)[0]
    [apply(asset, data["Properties"]) for asset in sel_asset]
    for asset in sel_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(asset, False)
'''