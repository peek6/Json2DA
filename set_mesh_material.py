# Script to point all meshes in a list to a new material instance (MI)
# Assumes all meshes have a single MI you want to replace and that you want all meshes point to the same MI
# TODO: support cases where meshes points to more than one MI
# TODO: support cases where different meshes point to different MIs

# Usage:
#  - Set your mod dir in mod_dir
#  - list your meshes (including the paths, from your mod_dir root) in meshes_to_mod
#  - specify the new MI you want the mesh to point to in material_instance_path_and_name


import json
import unreal
import importlib

import utils
importlib.reload(utils)

mod_dir = '/your_mod_dir/'

meshes_to_mod = [
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_AB.SK_HUM_F_Socks_Socks01_Master_AB',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_ABC.SK_HUM_F_Socks_Socks01_Master_ABC',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_ABCD.SK_HUM_F_Socks_Socks01_Master_ABCD',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_ABCDE.SK_HUM_F_Socks_Socks01_Master_ABCDE',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_ABCDEF.SK_HUM_F_Socks_Socks01_Master_ABCDEF',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_B.SK_HUM_F_Socks_Socks01_Master_B',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_BC.SK_HUM_F_Socks_Socks01_Master_BC',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_BCD.SK_HUM_F_Socks_Socks01_Master_BCD',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_BCDE.SK_HUM_F_Socks_Socks01_Master_BCDE',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_BCDEF.SK_HUM_F_Socks_Socks01_Master_BCDEF',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_C.SK_HUM_F_Socks_Socks01_Master_C',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_CD.SK_HUM_F_Socks_Socks01_Master_CD',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_CDE.SK_HUM_F_Socks_Socks01_Master_CDE',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_CDEF.SK_HUM_F_Socks_Socks01_Master_CDEF',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_D.SK_HUM_F_Socks_Socks01_Master_D',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_DE.SK_HUM_F_Socks_Socks01_Master_DE',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_DEF.SK_HUM_F_Socks_Socks01_Master_DEF',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_E.SK_HUM_F_Socks_Socks01_Master_E',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_EF.SK_HUM_F_Socks_Socks01_Master_EF',
    mod_dir+'SK_HUM_F_Socks_Socks01_Master_F.SK_HUM_F_Socks_Socks01_Master_F'
    ]

material_instance_path_and_name = mod_dir+'MI_HUM_F_Socks_suntan1.MI_HUM_F_Socks_suntan1'



new_material_instance = unreal.load_asset(material_instance_path_and_name)

for my_mesh in meshes_to_mod:
    print("Processing "+my_mesh)
    skeletal_mesh = unreal.load_asset(my_mesh) #mod_dir+'SK_HUM_F_Socks_Socks01_Master_AB.SK_HUM_F_Socks_Socks01_Master_AB')
    skeletal_mesh_materials = skeletal_mesh.materials

    material_array = unreal.Array(unreal.SkeletalMaterial)

    for material in skeletal_mesh_materials:

        new_sk_material = unreal.SkeletalMaterial()

        slot_name = material.get_editor_property("material_slot_name")
        material_interface = material.get_editor_property("material_interface")

        #if materials_to_change.get(str(slot_name)):
        #    material_interface = materials_to_change[str(slot_name)]

        new_sk_material.set_editor_property("material_slot_name", slot_name)
        new_sk_material.set_editor_property("material_interface", new_material_instance)

        material_array.append(new_sk_material)

    skeletal_mesh.set_editor_property("materials", material_array)
    unreal.EditorAssetLibrary.save_loaded_asset(skeletal_mesh, False)