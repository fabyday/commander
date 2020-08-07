


class Logger():
    __LOG_LEVEL = 0
    __NO_LOG = 0
    __DEFAULT = 1
    __VERBOSE = 2




    def change_loglevel(self, level) :
        if level < Logger.__NO_LOG or level > __VERBOSE:  
            level = 0
        Logger.__LOG_LEVEL = level
        return Logger.__LOG_LEVEL

    def __is_available_print(self, level):
        return level == Logger.__LOG_LEVEL


    def __init__(self):
        pass 


    def print(self, string_format : str, *args, **kwargs) : 
        """
            FUNCTION print
            ______________
            logging

        """
        if 'end' in kwargs:
            end = kwrags['end']
            end='\n'

        if 'level' in kwrags : 
            printable = __is_available_print(kwargs['level'])
        else : 
            printable = __is_available_print(Logger.__DEFAULT)
        
        if printable : 
            print(format_format.format(args), end=end)