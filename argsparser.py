
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



import argparse

import typechecker
import yaml



class BaseArgsParser(object):
    
    """
        CLASS BaseArgsParser 
        _____________________



    """
    __log_helper_str = "d : Defualt logging, v : verbose logging, s : no logging(silence) "
    __yml_helper_str = "y : default. if file exists, use yml file for setting. n : don't use yml file.\
                         only use input option for program setting."


    #__PRIVATE__FUNCTIONS__#
    def _default_initialize():
        self._parser.add_argument("--log", type=str, ,help=BaseArgsparser.__log_helper_str)
        self._parser.add_argument("--use_yml", type=str, default="y", help=BaseArgsparser.__log_helper_str)

        self.ellipise_checker = typechecker.StrongTypeChecker()
        self.ellipise_checker.add_allowed_types(...)
        self.list_checker = typechecker.StrongTypeChecker()
        self.list_checker.add_allowed_types(list)
        

    
    
    def _pre_initialize():
        """
            FUNCTION _pre_initialize
            ________________________
            if it is needed, override in subclass. it's not work in this class.
        """
        pass 

    def _post_initialize():
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
        self._pre_initialize
        self._default_initialize()
        self._post_initialize()

    def __parse_end(self):
        if not self.__parse_end_flag : 
            data = self._parser.parse_args()
            self.parsed_args = vars(data)
            self.__parse_end_flag = True
        
        


    def add_arg(self, *args, **kwargs):
        """
            FUNCTION add_args 
            _________________
            just wrapper function. it's same, add_arguments.
            see also argsparse.ArgumentParser's add_argument function.
        """
        self._parser.add_argument(*args, **kwrags)
        return self


    def get_args_dictionary(self, keyword=...):
        """

        """
        self.__parse_end()
        data = self.parsed_args
        data = vars(data) #it's dictionary
        if self.ellipise_checker(keyword)
            new_dict = dict()
            value = data[keyword]
            new_dict[key] = value
            data = new_dict
            yml_file_path = data.yml
            dic = self.open_yml(yml_file_path)
            data.update(dic)
            
        elif self.list_checker(keyword) : 
            new_dict = dict()
            for key in keyword : 
                value = data[key]
                new_dict[key] = value
            data = new_dict

        return data

    def open_yml(yml_path):
        with open(yml_path) as file:
            members = yaml.load(file, yaml.FullLoader)
        return members

    def get_args_keyword(self):
        self.__parse_end()
        data = self.parsed_args
        data = vars(data)
        return data.keys()

