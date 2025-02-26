import re

class HDLParser:
    def __init__(self, filename):
        # Initialise with a HDL file path
        self.filename = filename
        self.modules = {}  # Dictionary for parsed modules

    # Need to sanitise the input file to remove comments, check for syntax errors, check for missing modules, insure there are no brackets in variable names
    def parse(self):  # Need to add functionality for hdl files being able to include other hdl files
        # Reads HDL file and parses it by extracting module definitions
        with open(self.filename, "r") as file:
            content = file.read()
        module_pattern = re.findall(r"MODULE (\w+)\((.*?) -> (.*?)\)(.*?)END", content, re.DOTALL)  # \( and \) match literal parentheses
        for module in module_pattern:
            name, inputs, outputs, body = module

            input_list = [module_input.strip() for module_input in inputs.split(",")]  # Separates the inputs
            output_list = [module_output.strip() for module_output in outputs.split(",")]  # Separates the outputs

            body_statements = re.findall(r"(\w+)\s*=\s*(.+);", body)  # Extracts the body statements and separates them into a list of tuples

            self.modules[name] = {
                "inputs": input_list,
                "outputs": output_list,
                "body": body_statements
            }
            # print(body_statements) 
        return self.modules

def main():
    parser = HDLParser("examples/gates.hdl")
    modules = parser.parse()
    print(modules)

if __name__ == "__main__":
    main()