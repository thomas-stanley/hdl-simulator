from lark import Lark, Transformer
from .module import Module

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

class HDLParser:
    def __init__(self):
        self.parser = Lark(hdl_grammar, parser="lalr")
        self.transformer = HDLTransformer()
    
    def parse(self, filename):
        try:
            with open(filename, "r") as file:
                text = file.read()
            tree = self.parser.parse(text)
            return self.transformer.transform(tree)
        except ValueError:
            raise ValueError(f"File '{filename}' not found.")

def main():
    parser = HDLParser()
    modules = parser.parse("examples/gates.hdl")
    for module in modules:
        print(module)

if __name__ == "__main__":
    main()