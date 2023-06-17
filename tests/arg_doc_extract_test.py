import re
args="""param_a: the first parameter"""

# 匹配参数类型可以不指定
arg_doc_list = re.findall(r'(\w+)(\((\w+)\))?:\s*(.*)', args)

print(arg_doc_list)