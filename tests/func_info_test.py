# param_a: the first parameter
def test_function(param_a: str, param_b: int, param_c: int, l: list) -> str:
    """
    Function for testing.

    Args:
        param_a(str): the first parameter
        param_b(int): the second parameter
        param_c(int): the third parameter
        l(list[int]): the list parameter

    Returns:
        str: the return value
    """

    return "test_function"

import re
import inspect

print(test_function.__annotations__)
print(test_function.__doc__)
print(test_function.__name__)

print(inspect.getfullargspec(test_function))
print(inspect.signature(test_function).parameters.values())

params = enumerate(inspect.signature(test_function).parameters.values())
for i, param in params:
    print(i, param.name, param.kind, param.default, param.annotation, param.annotation.__name__)
    if param.annotation.__name__ == "list":
        array_type = re.findall(r'list\[(\w+)\]', str(param.annotation))
        print(array_type)

print(inspect.Parameter.empty)

doc = inspect.getdoc(test_function)
print(doc)

# extract doc of args from docstring
import re

doc_spt = doc.split('\n\n')
desc = doc_spt[0]
args = doc_spt[1]
returns = doc_spt[2]

print(desc)

arg_doc_list = re.findall(r'(\w+)\(([\w\[\]]+)\):\s*(.*)', args)
print(arg_doc_list)

