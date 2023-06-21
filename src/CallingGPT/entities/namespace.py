import sys
import re
import inspect


def get_func_schema(function: callable) -> dict:
    """
    Return the data schema of a function.
    {
        "function": function,
        "description": "function description",
        "parameters": {
            "type": "object",
            "properties": {
                "parameter_a": {
                    "type": "str",
                    "description": "parameter_a description"
                },
                "parameter_b": {
                    "type": "int",
                    "description": "parameter_b description"
                },
                "parameter_c": {
                    "type": "str",
                    "description": "parameter_c description",
                    "enum": ["a", "b", "c"]
                },
            },
            "required": ["parameter_a", "parameter_b"]
        }
    }
    """
    func_doc = function.__doc__
    # Google Style Docstring
    if func_doc is None:
        raise Exception("Function {} has no docstring.".format(function.__name__))
    func_doc = func_doc.strip().replace('    ','').replace('\t', '')
    # extract doc of args from docstring
    doc_spt = func_doc.split('\n\n')
    desc = doc_spt[0]
    args = doc_spt[1] if len(doc_spt) > 1 else ""
    returns = doc_spt[2] if len(doc_spt) > 2 else ""

    # extract args
    # delete the first line of args
    arg_lines = args.split('\n')[1:]
    arg_doc_list = re.findall(r'(\w+)(\((\w+)\))?:\s*(.*)', args)
    args_doc = {}
    for arg_line in arg_lines:
        doc_tuple = re.findall(r'(\w+)(\(([\w\[\]]+)\))?:\s*(.*)', arg_line)
        if len(doc_tuple) == 0:
            continue
        args_doc[doc_tuple[0][0]] = doc_tuple[0][3]

    # extract returns
    return_doc_list = re.findall(r'(\w+):\s*(.*)', returns)

    params = enumerate(inspect.signature(function).parameters.values())
    parameters = {
        "type": "object",
        "required": [],
        "properties": {},
    }


    for i, param in params:
        param_type = param.annotation.__name__

        type_name_mapping = {
            "str": "string",
            "int": "integer",
            "float": "number",
            "bool": "boolean",
            "list": "array",
            "dict": "object",
        }

        if param_type in type_name_mapping:
            param_type = type_name_mapping[param_type]

        parameters['properties'][param.name] = {
            "type": param_type,
            "description": args_doc[param.name],
        }

        # add schema for array
        if param_type == "array":
            # extract type of array, the int of list[int]
            # use re
            array_type_tuple = re.findall(r'list\[(\w+)\]', str(param.annotation))

            array_type = 'string'

            if len(array_type_tuple) > 0:
                array_type = array_type_tuple[0]

            if array_type in type_name_mapping:
                array_type = type_name_mapping[array_type]

            parameters['properties'][param.name]["items"] = {
                "type": array_type,
            }

        if param.default is inspect.Parameter.empty:
            parameters["required"].append(param.name)

    return {
        "function": function,
        "description": desc,
        "parameters": parameters,
    }


class Namespace:
    """
    Namespace is a virtual container for functions, generated automatically by CallingGPT
    with user provided modules.
    """

    modules: list = []
    
    functions: dict = {}
    """Store functions with structure as follows:
    {
        "module_name_a": {
            "function_name_a": {
                "function": function_a,
                "description": "function_a description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parameter_a": {
                            "type": "str",
                            "description": "parameter_a description"
                        },
                        "parameter_b": {
                            "type": "int",
                            "description": "parameter_b description"
                        },
                        "parameter_c": {
                            "type": "str",
                            "description": "parameter_c description",
                            "enum": ["a", "b", "c"]
                        },
                    },
                    "required": ["parameter_a", "parameter_b"]
                }
            },
        }
    }

    """

    def _retrieve_functions(self):
        self.functions = {}
        for module in self.modules:
            # assert module is a module
            assert isinstance(module, type(sys))
            # ignore non-function attributes
            if not hasattr(module, '__functions__'):
                functions = {k: v for k, v in module.__dict__.items() if callable(v)}
                # ignore private functions
                functions = {k: v for k, v in functions.items() if not k.startswith('_')}
            else:
                functions = {v.__name__: v for v in module.__functions__ }

            self.functions[module.__name__.replace(".","-")] = {}

            for name, function in functions.items():
                funtion_dict = get_func_schema(function)

                self.functions[module.__name__.replace(".","-")][name] = funtion_dict

    def __init__(self, modules: list):
        self.modules = modules
        self._retrieve_functions()

    @property
    def functions_list(self):
        result: list = []
        for module_name, module in self.functions.items():
            for function_name, function in module.items():
                func = function.copy()
                func["name"] = "{}-{}".format(module_name, function_name)
                del func["function"]
                result.append(func)

        return result
    
    def call_function(self, function_name: str, args: dict):
        """
        Call a function by name.
        """
        result = {}

        # split the function name
        fn_spt = function_name.split('-')
        module_name = '-'.join(fn_spt[:-1])
        function_name = fn_spt[-1]

        # get the function
        function = self.functions[module_name][function_name]['function']

        # call the function
        result = function(**args)

        return result
    
    def add_function(self, module_name: str, function: callable):
        """
        Add a function to namespace.
        """
        # assert isinstance(function, callable)
        if module_name not in self.functions:
            self.functions[module_name] = {}
        self.functions[module_name][function.__name__] = get_func_schema(function)

    def add_modules(self, modules: list):
        """
        Add a module to namespace.
        """
        self.modules.extend(modules)
        self._retrieve_functions()
    