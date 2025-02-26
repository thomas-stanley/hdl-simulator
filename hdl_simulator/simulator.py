from parser import HDLParser

class CircuitSimulator:
    def __init__(self, filename):
        # Parses the HDL file and initialises the simulator with the parsed modules
        self.parser = HDLParser(filename)
        self.modules = self.parser.parse()  # Parsed modules stored here

    def evaluate(self, module_name, inputs):
        # Evaluates a module given its name and inputs
        if module_name == "Nand":  # Special, hard-coded, case for the Nand gate to improve performance
            if len(inputs) != 2:
                raise ValueError(f"Expected 2 inputs for {module_name} module, got {len(inputs)}.")

            return {"out": int(not(inputs["a"] and inputs["b"]))}
        
        if module_name not in self.modules:
            raise ValueError(f"Module {module_name} not found.")

        module = self.modules[module_name]  # Fetch the module from the parsed modules
        input_variables = module["inputs"]
        output_variables = module["outputs"]
        logic = module["body"]
        variables = inputs.copy()  # Copy the inputs to the output values

        if len(input_variables) != len(inputs):
            raise ValueError(f"Expected {len(input_variables)} inputs for {module_name} module, got {len(inputs)}.")
        
        for line in logic:
            variable, expression = line
            if "Nand" in expression:
                arguments = expression.split("(")[1].split(")")[0].split(",")  # Splits and includes after open brackets, splits then includes before close brackets, then splits by commas
                arguments = [arg.strip() for arg in arguments]  # Removes whitespace
                variables[variable] = int(not (variables[arguments[0]] and variables[arguments[1]]))
                # Need some sort of recursion or something like that to evaluate the Nand gate for higher level modules

        return {out: variables[out] for out in output_variables}                

def main():
    simulator = CircuitSimulator("examples/gates.hdl")
    inputs = {"a": 1, "b": 0}
    # inputs = {"a": 0}
    outputs = simulator.evaluate("Xor", inputs)
    print(outputs)

if __name__ == "__main__":
    main()
        

        

        


