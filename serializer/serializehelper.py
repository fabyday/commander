from . import serialize
from ..envhelper.env import DirectoryEnvironment

env = DirectoryEnvironment

class SerializeHelper():
    def __init__(self, input_env, output_env, cls_or_func):
        """
            cls_or_func : main data process
        """

        self.input_env = input_env
        self.output_env = output_env
        self.cls_or_func = cls_or_func




    def compile(self):
        pass



    def run(self):
        previous = None
        for path in self.input_env:
            if previous != path  previous != None :
            self.cls_or_func(idx)
            pass





    
