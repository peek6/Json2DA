
class Material:
    def __init__(self, asset_path, asset_name, json_path):
        self.asset_path = asset_path
        self.asset_name = asset_name
        self.asset_type = 'Material'
        self.json_path = json_path
        self.children = {} # dictionary keyed by asset name of the immediate children of this material
        self.data = {} # data list of parameters compatible with method to create the material in UE
        self.data_dict = {} # data dictionary of parameters for easier merging (to avoid duplicate parameters)

class MaterialInstance:
    def __init__(self, asset_path, asset_name, json_path):
        self.asset_path = asset_path
        self.asset_name = asset_name
        self.asset_type = 'MaterialInstanceConstant'
        self.json_path = json_path
        self.children = {}  # dictionary keyed by asset name of the immediate children of this material instance
        self.parent = None # pointer to parent object of this MI
        self.data = {} # data list of parameters compatible with method to create the material instance in UE
        self.data_dict = {} # data dictionary of parameters for easier merging (to avoid duplicate parameters)

