from __future__ import absolute_import

import os 
import logging

import re

import copy

#SORTING_OPTIONS
ASCENDING = 0
DESCENDING = 1
COMMON_NAME = 2

#SAVE_OPTIONS
SAVE_SAME_AS_ORIGINAL = 0
SAVE_EACH_PRIORITY = 1




class PathEntity():
    """
        Class PathEntity : 
            encapsulated Path. 
    """
    def __init__(self, basepath="", category_path=[""], target_name_path = ""):
        """
            ARGS :
                ( String ) basepath : basepath := working_directory + target_directory.
                ( List of String ) category_path : child of base path.
                ( String ) target_name_path : child of category_path. it is real file path.

        """
        self.basepath = basepath
        self.category_path = category_path
        self.target_name_path = target_name_path
        self.end_flag = False



    def __call__(self):
        return os.path.join(self.basepath, *self.category_path, self.target_name_path)


class DirectoryEnvironment(object):
    """
        Class DirectoryEnvironment : 
            Usage : 
                input_obj1 = DirectoryEnvironment(target_path= ..., copy_option_from_reference=None).omit_depth(...).set_target_object(...).compile()
                                            or 
                output_obj2 = DirectoryEnvironment(target_path= ..., copy_option_from_reference={obj1} ).compile()


    """
    def __initialize_vars(self):
        self.working_directory = None
        self.target_path = None #if Change this you can easily make output path
        self.recompile_flag = False
        self.base_path = None

        #OMIT
        self.omit_desired_depth = None
        self.omit_flag = False

        #REGEX
        self.target_name_regex = None
        self.re = None 

        #DATA
        self.raw_data_pathes = None
        self.copy_detected = False
        self.copy_obj = None 
        self.omitted_data_set_idx = 0
        self.omitted_data_set = None # remove overlapped names.
        #SORT
        self.search_depth = None
        self.sort_option = DESCENDING

        #GENERATOR OBJECT
        self.generator_obj = None

        self.sep = os.path.sep


    def __init__(self, target_path, working_directory="./", copy_option_from_reference=None):
        """
            Method __init__ : 
            - args 
                (str) target_dir : absolute path or reletive path. if it is reletive path, current dir is depend on working_directory argument.
                (str) working_directory : set current directory path. if target_dir is abs path. working directory path is basepath of target_dir
                (DirectoryEnvironment) copy_refrence : refer to 
                bool target_dir_gen : if target path is not exists, make dir recursively.

        """
        
        #initialize all Variables.
        self.__initialize_vars()


        self.working_directory = os.path.abspath(working_directory)

        
        self.target_path = os.path.normpath(target_path)
        if os.path.isabs(self.target_path) : 
            self.working_directory = os.path.dirname(self.target_path)
            self.target_path = os.path.basename(self.target_path)

        
        if not os.path.exists(os.path.join(self.working_directory, self.target_path)) :
            os.makedirs(os.path.join(self.working_directory, target_path))
        


        if copy_option_from_reference != None : 
            self.copy_detected = True
            self.copy_obj = copy_option_from_reference

            #TODO 
            # self.omit_depth(copy_option_from_reference.desired_depth)
            #     .set_target_object(copy_option_from_reference.target_name_regex)
            #     .set_options(copy_option_from_reference.sort_option)
            
        self.omit_depth(None)
        self.set_options()
    def omit_depth(self, desired_depth=None):
        """
            Method omit_depth : 
                -Args : 
                    (list of Integer & None ) desired_depth : it will start with 0, depth that you will omit. 0 means that target_path.
                                                    (ex. if exists two pathes. {path/to/temp1/some} , {path/to/temp2/some} -> omit_depth(2) -> {path/to/some} , {path/to/some})
                - Return
                    DirectoryEnvironment : self instance
                    

        """
        #TODO type checker list and Integer and None
        if desired_depth != None : 
            self.omit_flag = True
        if type(desired_depth) != list:
            desired_depth = [desired_depth]

        self.omit_desired_depth = desired_depth

        return self

    def set_target_object(self, target_name_regex=None):
        """
            Method set_target_object : 
                -Args : 
                    (string) target_name_regex : target_file regex string. it's not directory name. 
                -Retrun
                    DirectoryEnvironment : self instance         
        """

        self.target_name_regex = target_name_regex
        return self
    
    #정렬이 중요하지.. 파일의 길이를 일정하게 만들어주는 방법.
    def set_options(self, dir_search_depth = -1, sort_option=DESCENDING):
        if sort_option in [ASCENDING, DESCENDING, COMMON_NAME] : 
            self.sort_option = sort_option
        
        
        self.search_depth = dir_search_depth
        
        return self
         

    
    def compile(self):
        """
            Method compile :
            
            - args
                None
            
            - raise
                if not enough depth exists, it'll raise Error. automatically re-generate omit-depth or other options, but it make side-effect that is unexpected.

            - Return 
                    DirectoryEnvironment : self instance
        """
        self.base_path = self.get_base_path() #working dir & target_path 
        


        ################# MAIN EXTRACTING LINES ################################################
        #extract directory list. NOT FILES NAME LIST!!
        if self.copy_detected : 
            self.raw_data_patches = copy.deepcopy(self.copy_obj.raw_data_patches)
        else : 
            #TODO need some Exception or Error handling. it maybe occur some Bug. 
            self.raw_data_patches = self.__get_subdirectory(base_dir=self.base_path, depth = 0, parent_path = "")
            self.raw_data_patches = self.__sort_order_safety(self.raw_data_patches)
            self.raw_data_patches = self.remove_overlapped_dirname(self.raw_data_patches)
            self.raw_data_patches = self.__make_to_dictionary(self.raw_data_patches)

        #########################################################################################

        
        #Re-ORDER
        
        #regex initialize
        self.re = re.compile(self.target_name_regex)



        # #OMIT 
        if self.omit_flag : 
            self.raw_data_patches = self.__omit_path_mask(self.raw_data_patches)
            self.raw_data_patches = self.remove_overlapped_dirname(self.raw_data_patches)
            

        #TODO post processing may needed.
        

        
        return self

    def __make_to_dictionary(self, pathes):
        """
            pathes : [ [common/path1/some1] .... [common/path2/some2] ] 
            return 
                dictionary 
                {
                    some1 : [[common, path1, some1], [common, path2, some2]], 
                    some2 : [[common, path1, some2],  [common, path2, some2]]
                }
        """
        path_label_dict = dict()
        for path in pathes : 
            key = path[-1]
            if key not in path_label_dict:
                path_label_dict[key] = [path]
            else :
                path_label_dict[key].append(path)
        
        return path_label_dict

    def find_path_from_dict(self, path):
        """
            ARGS :
                path [path, to, some1]
                inner path dict {
                                    some1 : [ [path, to], [path2, to] ] 
                                }
            RETURN : 
                [path, to, some1]
        """
        key = path[-1]
        prefix = self.raw_data_patches[key]
        prefix.append(key)
        path = self.omit_path(prefix) # if Path omitted. omitted path is removed.
        return path 

    def remove_overlapped_dirname(self, data):
        
        data_list = []
        for names in data : 
            if names not in data_list :
                data_list.append(names)
        return data_list
                
    def exists(self, file_name):
        return os.path.exists( os.path.join(self.working_directory, self.target_path, file_name) )


    def __sort_order_safety(self, raw_pathes):
        """
            Method __sort_order_safety : 
            sort by Order Safely.
                -args : 
                    (list of string) raw_pathes : __get_subdirectory method return Values(list of pathes). 

        """
        #TODO
        reverse_flag = False
        if self.sort_option == DESCENDING :
            reverse_flag != reverse_flag

        print("raw len", len(raw_pathes))#, "\n", raw_pathes)
        sorted(raw_pathes, key=lambda x : x[-1], reverse = reverse_flag)
        return raw_pathes


    def get_base_path(self):
        """
            Method __get_base_path :
                -args :
                    None
                -Return :
                    (string) path : it's concat working_drectory and target_path. ex. work_dir = "./", and target_path="some_dir" -> return {"./some_dir"}
        """
        return os.path.join(self.working_directory, self.target_path)


    def __get_subdirectory(self, base_dir, depth = 0, parent_path = ""):
        """
            Method __get_subdirectory
                recursive
                path is list of string
                - Args : 
                    base_dir : working_directory + target_depth
                    depth : it's calculated from target_depth.
                    parent_path : parent path in working_directory and target directory

                
                - Return : 
                    [["path", "to", "some", "things1"], ["path", "to", "some", "things2"], .... ["path", "to", "some", "things_{n}"] ]

        """
        if not os.path.isdir(os.path.join(base_dir, parent_path)) or self.search_depth == depth :
            delim = os.path.sep
            # the reason why wrap this return value is for using extend method.
            result = parent_path.split(delim)[:-1]
            if result : # if result is empty, return empty list
                return [result] # list [ ['path', 'to', 'some' ..., 'where'], ['path', 'to', 'some' ..., 'where'] ]
            return []    
            
            
        
        # Result Must be 2-dimemsion list.
        path_list = []
        for child_path in os.listdir(os.path.join(base_dir, parent_path)):
            #Result := composite list like [[path, list], [path, list2]].
            results = self.__get_subdirectory(base_dir, depth+1, os.path.join(parent_path, child_path))
            

            path_list.extend(results)        
        return path_list



            


    def __omit_path_mask(self, path_dict):
        """
            Method __omit_path : 
                omit path base on Variable self.omit_desired_path
                -args : 
                    path : path calculated at __get_subdirectory. ex. ["C", "test", "path"] -> ["C", "path"]
                -return omited path_list 

        """ 


        for key in path_dict : 
            for idx in range(len(path_dict[key])) :
                path_dict[key][idx] = self.omit_path(path_dict[key][idx])
        return path_dict
    
    def omit_path(self, path):
        
        """
            RETURN
                ['some','path','to']
        """
        path_str = []       
        for idx in range(len(path)) :
            if idx in self.omit_desired_depth : 
                continue
            path_str += [path[idx]]
        return path_str


    def __iter__(self):
        self.generator_obj = self.__generator()
        return self

    def __next__(self):
        """
            return basepath, item_path
            
        """
        return next(self.generator_obj)
            
    def __get_subfile(self, base_path, child=""): 
        """
            Method __get_subfile : 
                - Args : 
                    path : directory absolute path which want to find files.
                - Return : 
                    path_list : path lists : ["path/to/file1", "path/to/file2", ..., "path/to/file_{n}"]
        """
        path = os.path.join(base_path, child)
        # Return Value is ["path/to/file"] or []
        if not os.path.isdir(path) : 
            if self.re.search(path) :
                return [child]
            return []

        # if it's Dir
        path_list = []
        for item in os.listdir(path) : 
            path_list.extend( self.__get_subfile( base_path, os.path.join(child, item) ) )
        
        return path_list        

    def __generator(self):
        """
            Method __generator :
                make generator when function __iter__ was called.
        """
        
        

        for  category_key in (self.raw_data_patches) : 
            path_list = self.raw_data_patches[category_key]
            for path in path_list : 
                dir_path = os.path.join(self.base_path, *path) # abs path.
                # for p in  :
                sub_file_path = self.__get_subfile(dir_path)
                for  complete_path in (sub_file_path) :
                    

                    yield PathEntity(self.base_path, path, complete_path)
                
    


    def transform_path_entity(self, path_entity):
        """
            transform path Entity to Current(Output Env) Path
        """
        path_entity.basepath = self.base_path
        input_category_path = path_entity.category_path
        
        path_entity.category_path = self.omit_path(input_category_path)
        
        path_precondiction = os.path.dirname(path_entity())
        if not os.path.exists(path_precondiction):
            os.makedirs(path_precondiction)

        return path_entity