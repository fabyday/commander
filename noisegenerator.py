import numpy as np





#C TYPE LOAD LIBRARY
import ctypes as ct






class NoiseGenerator(object):
    """
        Class HoleNoiseGenerator
            this class is C/C++ dynamic Libary wrapper Class.

            
    """

    def __initialize_vars(self):
        #NOISE CONFIGURATIONS
        self.noise_type = None
        self.noise_ratio = None

        # FUNCTION HANDLING VARS
        self.add_noise = None
        self.calc_normal = None 

    def __init__(self, noise_ratio = 0.01, noise_type ="gausian"):
        """
            
        """
        self.noise_ratio = noise_ratio
        self.noise_type = noise_type
        pass

    
    def __wrapper_function_initialize(self):
        native_func_pkg = ct.cdll.LoadLibrary("libnoise.dll")
        self.add_noise = native_func_pkg.add_noise
        self.calc_normal = native_func_pkg.calc_normal
        

    def compile(self):
        """
            Method compile()
        """        
        return self

    def __call__(self, file_name):
        """
            Method __call__

                -Args
                    (string) file_name : file_name which you want to generate.
                -Return
                    (v, f) generated_data
        """
        return (None, None) # TODO



class HoleNoiseGenerator():

    """
        Class HoleNoiseGenerator
            this class is C/C++ dynamic Libary wrapper Class.


    """
    def __initialize_vars(self):
        pass 

    def __init__(self, eye_vector):
        pass 

    def __wrapper_function_initialize(self):
        native_func_pkg = ct.cdll.LoadLibrary("libnoise.dll")

    def compile(self):
        """
            Method compile()
        """
        return self

    def __call__(self, file_name):
        return (None, None) # TODO






