import unreal
import MaterialExpressions
from utils import try_create_asset

MEL = unreal.MaterialEditingLibrary

def create_named_parameter(mat, name, ty, x, y):
    node = MEL.create_material_expression(mat, ty, x, y)
    node.set_editor_property("ParameterName", name)
    return node 

def create_parameter_array(mat, name, ty, num, originX = 0, originY = 0, X_SPACE=0, Y_SPACE=250):
    nodes = [
        create_named_parameter(mat, f"{name}[{i}]", ty, originX + X_SPACE * i, originY + Y_SPACE * i)
        for i in range(1, num + 1)
    ]
    return nodes

def getScalarOutput(node):
    if isinstance(node, (MaterialExpressions.TextureSampleParameter2D, MaterialExpressions.VectorParameter)):
        return "R"

    return ""
    

def connectNodesUntilSingle(mat, _nodes : list):
    nodes = [*_nodes]

    y = 0

    while len(nodes) > 1:
        nodeA, nodeB = nodes[:2]
        nodes = nodes[2:]
        connector = MEL.create_material_expression(mat, MaterialExpressions.Add, 200, y)
        MEL.connect_material_expressions(nodeA, getScalarOutput(nodeA), connector, "A")
        MEL.connect_material_expressions(nodeB, getScalarOutput(nodeB), connector, "B")
        nodes.append(connector)
        y += 75

    if not nodes:
        return None #  print("WARNING: There are no nodes in Material")
    else:
        return nodes[0]

def create_node_modular(mat, ty, yPos, name, defaultValue, slot_name):
    Y_GAP = 175
    node = MEL.create_material_expression(mat, ty, 0, yPos * Y_GAP)
    node.set_editor_property("ParameterName", name)
    if defaultValue is not None: node.set_editor_property(slot_name, defaultValue)
    return node


def generateInputNodes_modular(mat, data: dict):
    # Store last nodes (not always same as parameter nodes)
    all_final_nodes = []

    for p in data["ScalarParameterValues"]:
        all_final_nodes.append(
            create_node_modular(mat, MaterialExpressions.ScalarParameter, len(all_final_nodes), p["ParameterInfo"]["Name"],
                        p["ParameterValue"], "DefaultValue")
        )

    for p in data["VectorParameterValues"]:
        all_final_nodes.append(
            create_node_modular(mat, MaterialExpressions.VectorParameter, len(all_final_nodes), p["ParameterInfo"]["Name"],
                        unreal.LinearColor(p["ParameterValue"]["R"], p["ParameterValue"]["G"], p["ParameterValue"]["B"],
                                           p["ParameterValue"]["A"]), "DefaultValue")
        )

    for p in data["TextureParameterValues"]:

        # print("Processing "+p["ParameterValue"]["ObjectName"])
        if not (p["ParameterValue"] is None):
            obj_type, obj_name = p["ParameterValue"]["ObjectName"].split("'")[:2]
            # print("Received object with type "+obj_type)
            # print("Received object with name "+obj_name)

            print(f"Processing texture {obj_name}...")
            obj_path = p["ParameterValue"]["ObjectPath"]
            print(f"Path={obj_path}")

            full_path = obj_path.split(".")[0] + "." + obj_name
            asset = unreal.load_asset(f"{obj_type}'{full_path}'")

            if asset is None:
                folder = "/".join(obj_path.split(".")[0].split("/")[:-1])
                asset = try_create_asset(folder, obj_name, obj_type)
                print(asset)
                if asset is not None:
                    unreal.EditorAssetLibrary.save_loaded_asset(asset, False)

            slot_name = p["ParameterInfo"]["Name"]

            print(f"Adding texture {full_path} to slot {slot_name}")

            node = create_node_modular(mat, MaterialExpressions.TextureSampleParameter2D, len(all_final_nodes),
                               p["ParameterInfo"]["Name"], asset, "Texture")

            # node.set_editor_property(slot_name, asset)

            node.set_editor_property("SamplerSource", unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS)

            all_final_nodes.append(
                node
            )

    return all_final_nodes