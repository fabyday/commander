

class WeakTypeChecker(object) : 
    """
        Class WeakTypeChecker
        WeakTypeChecker check primary type and reference type. but it's not support inside of reference.
        Feature 
            - support fast mutiple type checking
            - unsupport to check reference Type's inner type.
        
    """
    
    def __init__(self) : 
        """
            Constructor __init__ 
            _____________________
            - Args 
                None 
            - Return
                None

        """
        self.__allowed_data_type = dict()
        self.__num_key = 0



    def _check_type(self, data): 
        """
            FUNCTION _check_type
            ____________________
            -args 
                data : type or object
            - return 
                type
        """
        datatype=type(data)

        if datatype is type : 
            return datatype
        return datatype     

    def add_allowed_type(self, example_data):
        """
            Function add_allowed_type
            _________________________
            - Args 
                example_data : example data structure that want to allowed.
            - Return
                (Int) key : return Key value.

        """
        #TODO check overlapped type.
        def alloc_key() :
            self.__num_key += 1 
            return self.__num_key
        

        datatype = self._check_type(example_data)
        key = alloc_key()
        self.__allowed_data_type[key] = datatype 

        return self
    
    def add_allowed_types(self, *example_data):
        for data in example_data : 
            self.add_allowed_type(data)
        return self
        
    def __is_allowed_type(self, data):
        
        return self._check_type(data) in self.__allowed_data_type.values()
    
    def __call__(self, data) : 
        return self.__is_allowed_type(data)


class StrongTypeChecker(WeakTypeChecker) : 
    """
        Class StrongTypeChecker
        StrongTypeChecker check primary type and also check inside of refrence types. like dict, list, tuple, set
        since StrongTypeChecker check inside of reference, type that inside of refrence must be same type.
        it's not allowed in StrongTypeChecker. example) [[], 1, 2] -> (translate) -> list(list(), Integer, Integer) X      
                                                        [[1], [2],[3]] -> (translate) -> list(list(Integer), list(Integer), list(Integer)) O
        -Feature 
            -Support inner type checking but it might be slow than WeakTypeChecker Class
            -Not Yet Support User Defined Class. it only allow to check Dictionary, List, Tuple, Set
        
    """
    __container_type = [dict, list, tuple, set]
    def __init__(self) : 
        """
            Constructor __init__ 
            _____________________
            - Args 
                None 
            - Return
                None

        """
        self.__allowed_data_type = dict()
        self.__num_key = 0



    def _check_type(self, data): 
        """
            FUNCTION _check_type
            ____________________
            -args 
                inputs : type or object
            - return 
                type
        """
        def recursive_container_checker(data_container):
            dictionary_flag = False
            
            if not type(data_container) in StrongTypeChecker.__container_type : 
                return type(data_container)

            if type(data_container) == dict:
                dictionary_flag = True
            
            prev_data_type = None
            for data in data_container:
                if dictionary_flag == True :
                    key_type = recursive_container_checker(key)
                    val_type = recursive_container_checker(data_container[key])
                    data_type = [key_type, val_type]
                else : 
                    data_type=[ recursive_container_checker(data) ]
                
                if prev_data_type == None : 
                    prev_data_type = data_type
                    continue
                
                if prev_data_type == data_type :
                    prev_data_type = data_type
                else :
                    raise TypeError("Type is Not Same.")
                print("w",prev_data_type)
                return prev_data_type
                
        
        datatype = super(StrongTypeChecker, self)._check_type(data)

        if datatype in StrongTypeChecker.__container_type : 
            datatype = recursive_container_checker(data)

        return datatype     

    def add_allowed_type(self, example_data):
        """
            Function add_allowed_type
            _________________________
            - Args 
                example_data : example data structure that want to allowed.
            - Return
                (Int) key : return Key value.

        """
        #TODO check overlapped type.
        def alloc_key() :
            self.__num_key += 1 
            return self.__num_key
        

        datatype = self._check_type(example_data)
        key = alloc_key()
        self.__allowed_data_type[key] = datatype 

        return self
    
    def add_allowed_types(self, *example_data):
        for data in example_data : 
            self.add_allowed_type(data)
        return self
        
    def __is_allowed_type(self, inputs):
        
        return inputs in self.__allowed_data_type.values()
    
    def __call__(self, inputs) : 
        return self.__is_allowed_type(inputs)

