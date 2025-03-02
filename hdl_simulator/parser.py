from lark import Lark, Transformer
from module import Module

hdl_grammar = """
    start: module+
    module: "MODULE" NAME "(" args "->" args ")" expr+ "END"
    args: NAME ("," NAME)*
    expr: NAME "=" function_call ";"
    function_call: NAME "(" args ")"
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    %import common.WS
    %ignore WS
"""

hdl_parser = Lark(hdl_grammar, parser="lalr")  # lalr is an efficient parser for this kind of text

class HDLTransformer(Transformer):

    def start(self, modules):
        return modules  # Currently warps it in a list even if there is only one of them but this seems to be fine for the time being

    def module(self, items):
        name, inputs, outputs, *body = items
        return Module(name, inputs, outputs, body)
    
    def expr(self, items):
        output_variable, function_call = items
        return (output_variable, function_call)  # Expressions stored as tuples
    
    def function_call(self, items):
        module_name, arguments = items  # May need to switch to *arguments if things stop working
        return {"module": module_name, "args": arguments}

    def args(self, items):
        return items
    
    def NAME(self, token):
        return token.value

def parse_hdl(filename):  # Might be worth rewriting as a class
    with open(filename, "r") as file:
        text = file.read()
    tree = hdl_parser.parse(text)  # Hdl text parsed into tree
    transformer = HDLTransformer()  # Create transformer
    return transformer.transform(tree)  # Tree to dictionary


def main():
    modules = parse_hdl("examples/gates.hdl")
    for module in modules:
        print(module)

if __name__ == "__main__":
    main()