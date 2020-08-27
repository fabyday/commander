import numpy as np





#C TYPE LOAD LIBRARY
import ctypes as ct




from commander.noise.geometry_noise import bummpy_noise

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

    def __init__(self, noise_ratio = 0.01, noise_type ="gausian", living_vertex_info = None):
        """
            
        """
        self.noise_ratio = noise_ratio
        self.noise_type = noise_type
        pass

    

    def compile(self):
        """
            Method compile()
            do nothing.
        """        
        
        return self

    def __call__(self, vertex_list, face_list, **kwargs):
        """
            Method __call__

                -Args
                    (3-dims or 2-dims : ndarray) vertex_list : vertex list 
                    (3-dim or 2-dims : ndarray) face_list : face list
                -Return
                    (v, f) generated_data
        """
        return bummpy_noise(vertex_list, face_list, noise_ratio = 0.015, living_vertex_info = None), face_list
        



class HoleNoiseGenerator():

    """
        Class HoleNoiseGenerator
            this class is C/C++ dynamic Libary wrapper Class.


    """
    def __initialize_vars(self):
        self.native_func_pkg = None
        

    def __init__(self, eye_vector):
        pass 

    def __wrapper_function_initialize(self):
        self.native_func_pkg = ct.cdll.LoadLibrary("libcnoise.dll")


    def compile(self):
        """
            Method compile()
        """
        return self

    def __call__(self, vertex, face):
        return (None, None) # TODO






