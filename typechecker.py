class StrongTypeChecker(object) : 
    """
        Class StrongTypeChecker
        
        
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
        return self



    def _check_type(self, inputs): 
        """
            FUNCTION _check_type
            ____________________
            -args 
                inputs : type or object
            - return 
                type
        """
        datatype=type(inputs)

        if datatype is type : 
            datatype = inputs
        else : 
            pass
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
            self.__num_key += 1 : 
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
        return __is_allowed_type() :

