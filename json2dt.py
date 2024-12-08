

import json
import unreal
import importlib

import utils

importlib.reload(utils)

from utils import apply
from pathlib import Path
# from parse_dt_json import fmodel_dt_json_to_ue_dt_json


import json

def fmodel_dt_json_to_ue_dt_json(json_path):
    with open(json_path.file_path, "r+") as fp:
        #with open(fmodel_json) as f:
        my_dict = json.load(fp)[0]
        # my_dict = json.load(f)[0]
        assert(my_dict["Type"]=="DataTable")
        dt_name = my_dict["Name"]
        #dt_path =
        struct_name = my_dict['Properties']['RowStruct']['ObjectPath'].split('.')[0]



        out_list = []
        for row in my_dict['Rows']:
            out_dict = {}
            out_dict['Name'] = row
            for col in my_dict['Rows'][row]:
                new_col = col # '_'.join(col.split('_')[:2])
                col_val = my_dict['Rows'][row][col]
                # print(col)
                if isinstance(col_val, dict) and 'ObjectPath' in col_val and 'ObjectName' in col_val:
                    # print('found dictionary asset reference')
                    obj_type, obj_name = col_val["ObjectName"].split("'")[:2]
                    full_path = col_val["ObjectPath"].split(".")[0] + "." + obj_name
                    col_val = f"{obj_type}'{full_path}'"
                out_dict[new_col] = col_val # my_dict['Rows'][row][col]
            out_list.append(out_dict)

        print('Original path is '+json_path.file_path)
        new_json = 'temp.json' # '\\'.join(json_path.file_path.split('\\')[:-1]+[(json_path.file_path.split('\\')[-1].split('.')[0]+'_for_UE'+'.json')]) # fmodel_json.split('\\')
        print('Writing UE formatted JSON to '+new_json)
        with open(new_json,'w') as fout:
            fout.write(json.dumps(out_list))
        #new_json = json.dumps(out_list)

    return struct_name, dt_name, new_json, my_dict, out_list

#fmodel_json = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\DynamicBone\DYB_ParamCSV_AML.json"
#struct_name, dt_name, new_json, my_dict, out_list = fmodel_dt_json_to_ue_dt_json(fmodel_json)

def main(json_path):
    print("=== JSON 2 Datatable ===")
    sel_asset = unreal.EditorUtilityLibrary.get_selected_assets()
    # print("Processing JSON file "+json_string)
    struct_name, dt_name, new_json, my_dict, out_list = fmodel_dt_json_to_ue_dt_json(json_path)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    print(sel_asset)

    full_asset_path_plus_name = str(sel_asset).split('"')[1]
    asset = unreal.load_asset(full_asset_path_plus_name)

    asset_path = '/'.join(full_asset_path_plus_name.split("/")[:-1])

    unreal.DataTableFunctionLibrary.fill_data_table_from_json_file(asset, new_json) #_path)

    #unreal.AssetRenameData(asset, new_package_path=asset_path, new_name=dt_name)
    unreal.EditorAssetLibrary.rename_asset(full_asset_path_plus_name, asset_path + "/" + dt_name)

    #for asset in sel_asset:
    unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

    # Path(new_json).unlink(missing_ok=True)