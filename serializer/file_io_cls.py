import commander.serializer.serialize as serialize
import commander.envhelper.env as env

class BaseFileIoClass():
    """
        Base Class File IO
    """
    def __init__(self):
        self.data = None

    def load_file(self, path_entity):
        result = dict()
        v, f = serialize.load_from_mesh(path_entity())
        result['v'] = v
        result['f'] = f
        return result
    
    def data_excute(self, data):
        return data

    def tmp_store(self, previous_data, data):
        self.data = data
        return self.data
    def tmp_load(self, data):
        return self.data


    def save_file(self, path_entity, data):
        serialize.save_to_mesh(path_entity(), **data)