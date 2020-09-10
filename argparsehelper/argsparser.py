
#                                    ___,,___
#                                 ,d8888888888b,_
#                             _,d889'        8888b,
#                         _,d8888'          8888888b,
#                     _,d8889'           888888888888b,_
#                 _,d8889'             888888889'688888, /b
#             _,d8889'               88888889'     `6888d 6,_
#          ,d88886'              _d888889'           ,8d  b888b,  d\
#        ,d889'888,             d8889'               8d   9888888Y  )
#      ,d889'   `88,          ,d88'                 d8    `,88aa88 9
#     d889'      `88,        ,88'                   `8b     )88a88'
#    d88'         `88       ,88                   88 `8b,_ d888888
#   d89            88,      88                  d888b  `88`_  8888
#   88             88b      88                 d888888 8: (6`) 88')
#   88             8888b,   88                d888aaa8888, `   'Y'
#   88b          ,888888888888                 `d88aa `88888b ,d8
#   `88b       ,88886 `88888888                 d88a  d8a88` `8/
#    `q8b    ,88'`888  `888'"`88          d8b  d8888,` 88/ 9)_6
#      88  ,88"   `88  88p    `88        d88888888888bd8( Z~/
#      88b 8p      88 68'      `88      88888888' `688889`
#      `88 8        `8 8,       `88    888 `8888,   `qp'
#        8 8,        `q 8b       `88  88"    `888b
#        q8 8b        "888        `8888'
#         "888                     `q88b
#                                   "888'
# MORE ... MORE TABACOO


# from __future__ import absolute_import


import argparse
# from commander.checker import typechecker
from ..checker import typechecker
import logging
import yaml



class BaseArgsParser(object):
    
    """
        CLASS BaseArgsParser 
            BaseArgsParser class work basic arguments like a YAML file, JSON, and arguments.
            if want to make Graphic User Interface Parser. inherit this Parser.
            Feature 
                it concern different level logging.
                it support hard type checking.
                basically supporting YAML Config or Setting file.

        _____________________

    """
    
    
    #__PRIVATE FUNCTION__#
    def __initialize_vars(self):
        #PARSER VARS DEFINITIONS#
        self._parser = None
        self.__parse_end_flag = None

        #TYPE_CHECKER VARS DEFINITIONS#
        self.ellipise_checker = None
        self.list_checker = None

        #RESULT SOTRED VAR
        self.parsed_data = None

        #LOGGING VARS DEFINITIONS#
        self.logger = None




    #__PROTECTED__FUNCTIONS__#
    def _default_initialize(self):
        """
            basic Function
        """
        
        # __PRE-DEFINED_ARGUMENTS__ #
        self._parser.add_argument("--log", type=str, default = 'd', choices =['d', 'v', 's'], help="d : Defualt logging, v : verbose logging, s : no logging(silence) ")
        
        # __FLAG_ARGUMENT__ # True or False
        self._parser.add_argument("-l", "--lock", action = "store_true",  help="lock setting property or User Defined Behavior. it helps to prevent User's Mistake.")
        self._parser.add_argument("-o","--overwrite", action = "store_true", help="yaml file properties overwrite parsing properties.")                                
        
        
        self._parser.add_argument("--yaml", type=str, default="test_phase1_plain.yml",help="yml file path.")                                
        



        
        
        # self.ellipise_checker = typechecker.StrongTypeChecker()
        # self.ellipise_checker.add_allowed_types(...)
        # self.list_checker = typechecker.StrongTypeChecker()
        # self.list_checker.add_allowed_types(list)
        

    def compile(self):
        """
        """
        #__PARSING__#        
        self._pre_initialize()
        self._default_initialize()
        self._post_initialize()
        self.parsed_data = self.__parse()

        
        #__PROCESSING__#
        # self.parsed_data = self.__yaml_extract(self.parsed_data)



        return self

    
    
    def _pre_initialize(self):
        """
            FUNCTION _pre_initialize
            ________________________
            if it is needed, override in subclass. it's not work in this class.
        """
        pass 

    def _post_initialize(self):
        """
            FUNCTION __post_initialize
            ________________________
            if it is needed, override in subclass. it's not work in this class.
        """
        pass 

    #__PUBLIC__FUNCTIONS__#

    def __init__(self,description=""):
        self._parser = argparse.ArgumentParser(description=description)
        self.__parse_end_flag = False

    def __parse(self):
        if not self.__parse_end_flag : 
            data = self._parser.parse_args()
            self.__parse_end_flag = True
            return vars(data)
        
        


    def add_arg(self, *args, **kwargs):
        """
            FUNCTION add_args 
            _________________
            just wrapper function. it's same, add_arguments.
            see also argsparse.ArgumentParser's add_argument function.
        """
        self._parser.add_argument(*args, **kwargs)
        return self


    def get_data(self):
        """
            Method get_data
                -Return 
                    (dictinary) data
        """
        
        if self.__parse_end_flag :
        
            return self.parsed_data
        raise ReferenceError("not compiled yet")

    def __open_yaml(self, yml_path):
        with open(yml_path) as file:
            members = yaml.load(file, yaml.FullLoader)
        return members

    def __yaml_extract(self, raw_parameter):
        yaml_key ="yaml"
        overwrite_key = "overwrite"
        if yaml_key in raw_parameter :
            yaml = raw_parameter[yaml_key] 
            raw_parameter.pop(yaml_key)
        else : 
            raw_parameter.pop(yaml_key)
            return raw_parameter
        
        yaml_data = self.__open_yaml(yaml)
        
        for key in yaml_data:
            if not raw_parameter[overwrite_key] and key in raw_parameter :
                continue
            raw_parameter[key] = yaml_data[key]
        
        #SAME CODE ABOVE
        # if raw_parameter[overwrite_key] :
        #     for key in yaml_data:
        #         raw_parameter[key] = yaml_data[key]
        # else : 
        #     for key in raw_parameter : 
        #         if key in raw_parameter : 
        #             continue 
        #         raw_parameter[key] = yaml_data[key]

        return raw_parameter
            
        
