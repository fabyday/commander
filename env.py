import os 
import typechecker
import logging
import glob
import re


class DirectoryManager(object) : 
    #SORTING_OPTIONS
    ASCENDING = 0
    DESCENDING = 1

    #SAVE_OPTIONS
    SAVE_SAME_AS_ORIGINAL = 0
    SAVE_EACH_PRIORITY = 1


    def __initialize_vars():
        """
        FUNCTION __initialize_vars 
        __________________________
        it shows all variables in this Class. even not initialized. 
        it's just definitions.
        """
        self.working_directory = ""
        self.base_path = ""
        self.priorities = []
        self.sort_priorities = []
        self.__file_circuit_list = []
        self.target_name_regex = ""
        self.re = None
        self.list_checker = typechecker.StrongTypeChecker().add_allowed_type(list)
        self.string_checker = typechecker.StrongTypeChecker().add_allowed_type(str)
    
    def __init__(self, base_path="", working_directory = "", target_name_regex=""):
        """
            - args 
                base_path : 
                working_directory : it's same as current directory. but you can change directory without moving real current directory.
                target_name_regex :

        """
        self.__initialize_vars()
        self.working_directory = os.path.curdir
        base_path = os.path.abspath(base_path)
        if os.path.exists(base_path) :
            self.base_path = base_path
        else : 
            raise EnvironmentError("PATH")
        
        if self.string_checker(target_name_regex) : 
            self.target_name_regex = target_name_regex


    def set_path_circuit_style(priorities=[0], sort_priorities=DirectoryManager.ASCENDING):
        """
            FUNCTION set_path_circuit_style
            _______________________________
            Assume that all path structure is same. all directory child is symmetric.
            -args 
                (List[Integer <- unsigned]) priorities : set searching priorities. if depth is shorter than given list. it ignores more than depth. : ex [0, 1, 2], [2, 1, 0]
                                                         default is [0].
                sort_priorities
                save_style : 
        """
        if self.list_checker(priorities) : 
            self.priorities = priorities
        self.sort_priorities = sort_priorities
    
    def compile(self):
        self.re = re.compile(self.target_name_regex) 
        

        stack = [] 
        
        child_path=glob.glob(self.base_path)
        stack.append(child_path)


        

    def excute_function(self, cls_or_func, *args, **kwrags):
        """
            Function proxy : 
            (Function) cls_or_func : class or function must be have path arguments.
        """
        for self.__file_circuit_list
            function(path=, *args, **kwrags)

    



