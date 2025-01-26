# Script to import material names from JSON into your Blender mesh

# Author:  peek6

# Usage:
#  - Set the mesh JSON path to the location of your exported mesh JSON from Fmodel.
#  - Select your imported gltf mesh in Blender
#  - Run the script in Blender

import json
import bpy

mesh_json_path = r"D:\modding\T8_kuo_mods\Exports\Polaris\Content\Mods\alisa_t_shirt_skirt\SK_alisa_t_shirt_skirt_msl.json"

#mesh_json_path = r"D:\modding\T8_kuo_mods\Exports\Polaris\Content\Mods\common_t_shirt_skirt\SK_common_t_shirt_skirt_msl.json"

#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\zbr\full_body\zbr_bdf_1p\meshes\SK_CH_zbr_bdf_1p_msl.json"

#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\mnt\full_body\mnt_bdf_1p_p\meshes\SK_CH_mnt_bdf_1p_p_msl.json"

#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\mnt\full_body\mnt_bdf_nike\meshes\SK_CH_mnt_bdf_nike_msl.json"

#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\mnt\full_body\mnt_bdf_1p\meshes\SK_CH_mnt_bdf_1p_v2_msl.json"

#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\hms\full_body\hms_bdf_1p\meshes\SK_CH_hms_bdf_1p_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\hms\full_body\hms_bdf_1p\meshes\SK_CH_hms_bdf_1p_v2_msl.json"

#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\hms\full_body\hms_bdf_bewitching\meshes\SK_CH_hms_bdf_bewitching_msl.json"

#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\der\full_body\der_bdf_yuzen_dogi\meshes\SK_CH_der_bdf_yuzen_dogi_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\mnt\face\mnt_fac\meshes\SK_CH_mnt_faceneck_msl.json"

#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\aml\face\aml_fac\meshes\SK_CH_aml_fac_msl.json"

#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\common\female\shoes\cmn_sho_f_loaferB\meshes\SK_CH_cmn_sho_f_loaferB_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\common\female\bottom\cmn_btm_f_pleatskirt\meshes\SK_CH_cmn_btm_f_pleatskirt_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\common\female\upper\cmn_bdu_f_tshirt\meshes\SK_CH_cmn_bdu_f_tshirt_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\common\female\upper\cmn_bdu_f_shirtribbon\meshes\SK_CH_cmn_bdu_f_shirtribbon_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\common\female\upper\cmn_bdu_f_blazerline\meshes\SK_CH_cmn_bdu_f_blazerline_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\aml\full_body\aml_bdf_miko\meshes\SK_CH_aml_bdf_miko_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\pgn\full_body\pgn_bdf_1p_p\meshes\SK_CH_pgn_bdf_1p_p_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\pgn\full_body\pgn_bdf_1p\meshes\SK_CH_pgn_bdf_1p_v1_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\unique\KAL\full_body\kal_bdf_1p_p\meshes\SK_CH_kal_bdf_1p_p_msl.json"
#mesh_json_path = r"D:\modding\T8_Demo\Exports\Polaris\Content\Character\Item\model\common\female\bottom\cmn_btm_f_bpleat\meshes\SK_CH_cmn_btm_f_bpleat_msl.json"
#mesh_json_path = r"D:\modding\T8_mods\Exports\Polaris\Content\Character\Item\model\unique\hms\full_body\hms_bdf_1p\meshes\SK_CH_hms_bdf_1p_v2_msl.json"

with open(mesh_json_path, "r+") as fp:
    data = json.load(fp)[0]["SkeletalMaterials"]

material_names = []

''' 
material_names = [
'MI_CH_femalebody_leg_skin',
'MI_CH_femalebody_body_skin',
'MI_CH_femalebody_arm_skin',
'MI_CH_femalebody_hand_skin'
]
'''

offset = 0

for ii in range(offset,len(data)):
    material_names.append(data[ii]['Material']['ObjectName'].split('\'')[1])


ii = 0
obj = bpy.context.object

#for obj in bpy.data.objects:
for num, m in list(enumerate(obj.material_slots)): #rename materials with . numbers
     if m.material:
         m.material.name = material_names[ii]
         ii = ii+1
         #print(m.material.name)

mats = bpy.data.materials

for obj in bpy.data.objects:
    for slt in obj.material_slots:
        part = slt.name.rpartition('.')
        if part[2].isnumeric() and part[0] in mats:
            slt.material = mats.get(part[0])
