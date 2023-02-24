import unreal
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

