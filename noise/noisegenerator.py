import numpy as np


import os 


# #C TYPE LOAD LIBRARY
# import ctypes as ct




from commander.noise.geometry_noise import bummpy_noise

class FreqNoiseGenerator(object):
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
        self.eye_vector = None
        self.valid_angular = None
        self.full_angle = 360


        self.x_rotate = None
        self.y_rotate = None
        self.z_rotate = None

        self.x_matrix = None
        self.y_matrix = None
        self.z_matrix = None

        self.rotate_term = None
        self.rotate_order = None

        self.__iteration_num = 0


    def __init__(self, 
                eye_vector, 
                valid_angular, 
                iterative_roation_size_x = 0, 
                iterative_roation_size_y = 0, 
                iterative_roation_size_z = 0,
                rotate_order = [0, 1, 2],
                rotate_term = [-1, -1, -1]
                ):
        """
        """
        self.__initialize_vars()
        self.eye_vector = eye_vector
        self.valid_angular = valid_angular
        self.x_rotate = iterative_roation_size_x
        self.y_rotate = iterative_roation_size_y
        self.z_rotate = iterative_roation_size_z
        
        self.rotate_order = rotate_order
        self.rotate_term = rotate_term
        

    def set_eye(self, eye_vector):
        """
            eye_vector : 3-dims vector
        """
        self.eye_vector = eye_vector
        return self
    
    def set_angular(self, valid_angular):
        """
            valid_angluar : scalar
        """
        self.valid_angular = valid_angular
        return self
    
    def set_roate( self, x_angle,
                         y_angle, 
                         z_angle, 
                         rotate_order = [0, 1, 2], 
                         rotate_term = [-1, -1, -1]
                         ):
        self.x_rotate = x_angle
        self.y_rotate = y_angle
        self.z_rotate = z_angle
        self.rotate_order = rotate_order
        self.rotate_term = rotate_term


    def __wrapper_function_initialize(self):
        # path = __file__
        # self.native_func_pkg = ct.cdll.LoadLibrary(os.path.join(path, "noisecpp", "build", "Release","noise.dll"))
        # self.addBackCullingNoise = self.native_func_pkg.addBackCullingNoise
        pass
    


    def __default_inner_data_initialize(self):
        self.__iteration_num = 0


    def compile(self):
        """
            Method compile()
        """

        if type(self.eye_vector) != np.ndarray : 
            self.eye_vector = np.array(self.eye_vector)
            
        self.eye_vector = self.eye_vector.reshape(1, -1)
        print(self.eye_vector, self.eye_vector.shape)
        assert len(self.eye_vector.shape) == 2, "it's not vector."
        self.eye_vector = self.eye_vector / np.linalg.norm(self.eye_vector) # process UNIT Vector
        self.valid_angular = self.valid_angular % self.full_angle
        
        
        self.__default_inner_data_initialize()
        
        


        #TODO
        return self

    def __get_normal_vector(self, vertice):
        """
            vertice : triangle vertex, shape 3 by 3. assume it as column vector.
        """
        
        #Calcuating Edge(Vector)
        
        v1 = vertice[0] - vertice[1]
        v2 = vertice[1] - vertice[2]

        # Normal Vector
        normal = np.cross(v1, v2)

        assert len(normal.shape) == 1, "wrong "
        return normal



    def __build_rotate_matrix(self):
        rot_x = self.__to_radian(self.x_rotate)
        rot_y = self.__to_radian(self.y_rotate)
        rot_z = self.__to_radian(self.z_rotate)
        x_matrix = np.array([   [1,             0,              0],
                                [0, np.cos(rot_x), -np.sin(rot_x)],
                                [0, np.sin(rot_x), np.cos(rot_x)]
                            ])
        y_matrix = np.array([   [np.cos(rot_y), 0, np.sin(rot_y)],
                                [0             , 1,            0],
                                [-np.sin(rot_y), 0, np.cos(rot_y)]
                            ])
        z_matrix = np.array([  [np.cos(rot_z), -np.sin(rot_z), 0],
                               [np.sin(rot_z), np.cos(rot_z), 0],
                               [0            , 0            , 1]
                            ])

        matrix_collection = [x_matrix, y_matrix, z_matrix]
        result_rotate = np.eye(x_matrix.shape[0]) # N x N shape identity matrix

        assert len(self.rotate_order) == 3, "out of size."
        for idx in self.rotate_order : 
            if self.rotate_term[idx] != -1 and self.__iteration_num % self.rotate_term[idx] == 0 : 
                result_rotate = result_rotate.dot( matrix_collection[idx] ) 

        return result_rotate


    def __to_radian(self, angle):
        return angle * np.pi / self.full_angle / 2  # pi/180 * angle = radian



    def __rotate_eye_vector(self) : 
        
        self.__iteration_num += 1 
        rotation = self.__build_rotate_matrix()
        
        result_eye = rotation.dot(self.eye_vector.T).T
        self.eye_vector = result_eye

    def __call__(self, vertex, face):
        """
            vertex : shape of (N, 3)
            face : shape of (M, 3)
        """
        assert len(vertex.shape) == 2, "vertex is not 2-dim matrix"
        assert len(face.shape) == 2, "face is not 2-dim matrix"

        
        vertex_size = vertex.shape[0]
        vertex_dim = vertex.shape[-1]

        face_size = face.shape[0]
        face_dim = face.shape[-1]
        #adj matrix
        neighbor_face = [[] for _ in range(vertex_size)]
        
        # Initialize adj matrix TODO exists, calcuating neighbor that make Simply . 
        for face_idx, face_row in enumerate(face) : 
            for vertex_num in face_row :
                neighbor_face[ vertex_num ].append( face_idx )
                

        #calculating Face Normal Vectors.
        face_normal = np.zeros_like(face).astype(np.float32)
        for idx, face_row in enumerate(face) : 
            normal = self.__get_normal_vector( vertex[face_row] ) 
            normal /= np.linalg.norm(normal, 2)
            face_normal[ idx, : ] = normal
        
        # Normal Per each Vertex.
        # TODO check libIGL. maybe exists, normal functions. now it is naive solution.
        vertex_normal = np.zeros_like(vertex)
        for idx in range(vertex_size) : 
            v_normal = np.mean( face_normal[neighbor_face[idx]], axis = 0 )
            v_normal /= np.linalg.norm(v_normal, 2)
            vertex_normal[ idx, : ] = v_normal



        radian = np.cos(self.valid_angular * np.pi / (self.full_angle/2) )


        vertex_angular = vertex_normal.dot(self.eye_vector.T)

        mask = vertex_angular < radian
        mask = mask.reshape(-1) #Shape [Vertex_size]
        mask = mask != False # switch False to True, True to False


        #tmporary for ... testing. if that vertex is hole info. it fills with 1.
        # vertex[mask] = np.array([1., 1., 1.])
        vertex[mask] = np.array([0., 0., 0.])

        result_vertex = vertex
        # result_vertex = vertex[mask]



        #post processing 
        self.__rotate_eye_vector()
        


        return result_vertex, face


            




