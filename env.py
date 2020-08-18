import os 
import typechecker
import logging
import glob
import re


#SORTING_OPTIONS
ASCENDING = 0
DESCENDING = 1
COMMON_NAME = 2

#SAVE_OPTIONS
SAVE_SAME_AS_ORIGINAL = 0
SAVE_EACH_PRIORITY = 1
class DirectoryManager(object) : 



    def __initialize_vars(self):
        """
        FUNCTION __initialize_vars 
        __________________________
        it shows all variables in this Class. even not initialized. 
        it's just definitions. you can see which variables exists in.
        """
        self.working_directory = ""
        self.target_path = ""
        self.priority_path = None
        self.priorities = []
        self.sort_priorities = []
        self.__file_circuit_list = []
        self.target_name_regex = ""
        self.re = None
        self.list_checker = typechecker.StrongTypeChecker().add_allowed_type(list)
        self.string_checker = typechecker.StrongTypeChecker().add_allowed_type(str)
        self.common_path = None
    
    def __init__(self, target_path="", working_directory = ".", target_name_regex=""):
        """
            - args 
                target_path : the directory that you want to work.
                working_directory : it's same as current directory. but you can change directory without moving real current directory.
                target_name_regex : regex for file name. it's usally find file. like txt file or ply file which you want to find.

        """
        self.__initialize_vars()
        

        if os.path.exists(working_directory) : 
            self.working_directory = os.path.abspath(working_directory)

        target_path = os.path.normpath(target_path)
        if os.path.exists(os.path.join(self.working_directory, target_path)) :
            self.target_path = target_path
        else : 
            raise EnvironmentError("the abs path for base path is not exists")
        
        if self.string_checker(target_name_regex) : 
            self.target_name_regex = target_name_regex


    def set_path_circuit_style(self, priorities=[0], sort_priorities=COMMON_NAME):
        """
            FUNCTION set_path_circuit_style
            _______________________________
            Assume that all path structure is same. all directory child is symmetric.
            -args 
                (List[Integer <- unsigned]) priorities : set searching priorities. if depth is shorter than given list. it ignores more than depth. : ex [0, 1, 2], [2, 1, 0]
                                                         default is [0].
                sort_priorities
        """
        if self.list_checker(priorities) : 
            self.priorities = priorities
        if sort_priorities in [ASCENDING, DESCENDING] : 
            self.sort_priorities = sort_priorities
        
    def compile(self):
        def get_priority_path(path, find_depth, depth=0):
            """
                recursive path find function
            """
            child_list = glob.glob(os.path.join(path,'*'))
            if find_depth == depth : 
                return child_list
            
            path_list = []
            for child in child_list :
                if os.path.isdir(child) :
                    result = recursive_path_iter(child, find_depth, depth=depth+1)
                    path_list.append(result)
                continue
            return path_list


        def get_target_file_path(target_path_list):
            """
                path find function using regex exp.
            """
            all_path = [] 
            for path in target_path_list : 
                tmp_path = glob.glob(path, "**", recursive=True)
                all_path.extend(tmp_path)
            
            for path in all_path :
                name = os.path.split(path)[-1]
                if self.re.match(name) == None : 
                    all_path.remove(path)

            return all_path
                    


            

        #regex compile
        self.re = re.compile(self.target_name_regex) 
        cur_priority = 0
        cur_priority_depth = self.priorities.index(cur_priority) # start 0 ~ N-1 
        


        #base path is root path.
        
        path = get_priority_path(self.target_path, find_depth=cur_priority_depth)
        #path/to/some1/b1 and path/to/some2/b1 ... common path is path/to/ + b1 = path/to/b1
        
        


        # PATH PREPROCESSING

        #[[pathes_1, ...], [[pathes_2, ...]]
        # merge path 
        path_group1 = path[0]
        path_group2 = path[1]
        #Common Path is ... if path exists like that "path/to/some1/dir1" and "path/to/some2/dir1" then common path is "path/to/".
        self.common_path = None
        while True:

            parent_path1 = os.path.split(path_group1[0])[0]
            parent_path2 = os.path.split(path_group2[0])[0]
            if parent_path1 == parent_path2 : 
                self.common_path = parent_path1
                break

        
        # PATH POSTPROCESSING
        # sort path by same name.
        sorted_path = dict()
        
        for idx in range(len(path)) : 
            path_group = path[idx]
            for tmp_path in path_group : 
                target_dir_name = os.path.split(tmp_path)[-1] # last directory name
                if target_dir_name in sorted_path : 
                    sorted_path[target_dir_name] = [ tmp_path ]
                else : 
                    sorted_path[target_dir_name].append(tmp_path)
        

        self.priority_path = sorted_path
        self.__file_circuit_list = dict()
        for key in self.priority_path:
            self.__file_circuit_list[key] = get_target_file_path(self.priority_path[key])

    def transfer_setting_only(self, env):
        pass
            


        

    def excute_function(self, cls_or_func, *args, **kwrags):
        """
            Function proxy : 
                this funtion is decorating function.
            - args
                (Function) cls_or_func : class or function must be have path arguments.
                args and kwrags : it is cls_or_func's arguments.
            - Return :
                return value is list type. [ val_1, val_2, val_3, ... val_n ]
        """
        return_list = []
        for key in self.__file_circuit_list:
            result = cls_or_func(path=self.__file_circuit_list[key], *args, **kwrags)
            return_list.append(result)
        return return_list

class DirectoryEnvironment(object):
    """
        Class DirectoryEnvironment : 
            Usage : 
                input_obj1 = DirectoryEnvironment(target_path= ..., copy_option_from_reference=None).omit_depth(...).set_target_object(...).compile()
                                            or 
                output_obj2 = DirectoryEnvironment(target_path= ..., copy_option_from_reference={obj1} ).compile()


    """
    def __initialize_vars():
        self.working_directory = None
        self.target_path = None #if Change this you can easily make output path
        self.recompile_flag = False

        self.omit_desired_depth = None
        self.search_depth = None
        self.sort_option = DESCENDING

        self.raw_data_pathes = None
        self.copy_detected = False


        self.copy_obj = None 
        
    def __init__(self, target_path, working_directory="./", copy_option_from_reference=None):
        """
            Method __init__ : 
            - args 
                (str) target_dir : absolute path or reletive path. if it is reletive path, current dir is depend on working_directory argument.
                (str) working_directory : set current directory path.
                (DirectoryEnvironment) copy_refrence : refer to 

        """

        if os.path.exists(working_directory) : 
            self.working_directory = os.path.abspath(working_directory)

        target_path = os.path.normpath(target_path)
        if os.path.exists(os.path.join(self.working_directory, target_path)) :
            self.target_path = target_path
        else : 
            raise EnvironmentError("the abs path for base path is not exists")


        if copy_option_from_reference != None : 
            self.copy_detected = True
            self.copy_obj = copy_option_from_reference

            #TODO 
            # self.omit_depth(copy_option_from_reference.desired_depth)
            #     .set_target_object(copy_option_from_reference.target_name_regex)
            #     .set_options(copy_option_from_reference.sort_option)
            
        
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

        self.omit_desired_depth = desired_depth
        return self

    def set_target_object(self, target_name_regex):
        self.target_name_regex = target_name_regex
        return self
    
    #정렬이 중요하지.. 파일의 길이를 일정하게 만들어주는 방법.
    def set_options(self, search_depth = -1, sort_option=DESCENDING):
        if sort_option in [ASCENDING, DESCENDING, COMMON_NAME] : 
            self.sort_option = sort_option
        
        
        self.search_depth = search_depth
         

    
    def compile(self):
    # def compile(self, recompile_flag = False):
        """
            Method compile :
            
            - args
                None
            
            - raise
                if not enough depth exists, it'll raise Error. automatically re-generate omit-depth or other options, but it make side-effect that is unexpected.

            - Return 
                    DirectoryEnvironment : self instance
        """
        base_path = self.__get_base_path() #working dir & target_path 
        



        
        #extract directory list. NOT FILES NAME LIST!!
        if not self.copy_detected : 
            self.raw_data_pathes = self.__get_subdirectory(base_path)
        else : 
            self.raw_data_patches = self.copy_option_from_reference.raw_data_patches



        #TODO post processing may needed.
        

        

            

        
        return self



    def __get_base_path(self):
        return os.path.join(self.working_directory, self.target_path)


    def __get_subdirectory(self, parent_path, depth = 0): 
        """
            recursive
            path is list of string
        """
        if not os.path.isdir(parent_path) or self.search_depth == depth :
            if depth == 0 : 
                return [""]
            else : 
                return [os.path.basename(parent_path)]
        
        
        path_list = []
        for child_path in os.listdir(parent_path):
            results = self.__get_subdirectory(os.path.join(parent_path, child_path), depth+1 )
            
            for result in results : 
                if depth == 0 :
                    path_list.append(result)
                else : 
                    path_list.append([parent_path].extend(result))
        
        return path_list



            


    def __omit_path_mask(self, path):
        """
            Method __omit_path : 
                omit path base on Variable self.omit_desired_path
                -args : 
                    path : path calculated at __get_subdirectory. ex. ["C", "test", "path"] -> ["C", "path"]
                -return omited path_list 

        """ 
        path_str = ""       
        for idx in range(len(path)) :
            if idx in self.omit_desired_depth : 
                continue
            path_str += path[idx]
        return path_str


            

        
    
    


    def __iter__(self):
        return self

    def __next__(self):
        pass
        

    



class DirectoryWorker(object):
    __CLS_OR_FUNC_LIST_STR='cls_or_func_list'
    __INPUT_ENV_STR = 'input_env'
    __OUTPUT_ENV_STR = 'output_env'
    def __init__(self):
        self.pipelines =dict()

    def add_pipeline(self, pipeline_name : str, cls_or_func_list, input_env, output_env):
        
        
        env = dict()
        env[DirectoryWorker.__CLS_OR_FUNC_LIST_STR] = cls_or_func_list
        env[DirectoryWorker.__INPUT_ENV_STR] = input_env
        env[DirectoryWorker.__OUTPUT_ENV_STR] = output_env
        self.pipelines[pipeline_name] = env
        



    
    def __call__(self):
        pass


