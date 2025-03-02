from parser import HDLParser

class CircuitSimulator:
    def __init__(self, filename):
        # Parses the HDL file and initialises the simulator with the parsed modules
        self.parser = HDLParser(filename)
        self.modules = self.parser.parse()  # Parsed modules stored here

    def evaluate(self, module_name, inputs):
        # Evaluates a module given its name and inputs
        if module_name == "Nand":
            if len(inputs) != 2:
                raise ValueError(f"Expected 2 inputs for {module_name} module, got {len(inputs)}.")

            return {"out": int(not(inputs["a"] and inputs["b"]))}
        
        if module_name not in self.modules:
            raise ValueError(f"Module {module_name} not found.")
        
        return {"out": self.evaluate_module(module_name, inputs)}
    
    def evaluate_module(self, module_name, inputs):
        if len(inputs) == 1:  # Fixes a bug that occurred when the only input for the not module was "b" and not "a" so was not able to be processed
            inputs = {"a": tuple(inputs.values())[0]}

        module = self.modules[module_name]
        input_variables = module["inputs"]
        # output_variables = module["outputs"] This will need to be sorted out when there are multiple outputs
        logic = module["body"]
        variables = inputs.copy()

        if len(input_variables) != len(inputs):
            raise ValueError(f"Expected {len(input_variables)} inputs for {module_name} module, got {len(inputs)}.")

        for line in logic:
            variable, expression = line
            function = expression.split("(")[0]
            arguments = expression.split("(")[1].split(")")[0].split(",")
            arguments = [arg.strip() for arg in arguments]

            if "Nand" == function:
                variables[variable] = int(not (variables[arguments[0]] and variables[arguments[1]]))
            else:
                variables[variable] = self.evaluate_module(function, {arg: variables[arg] for arg in arguments})
        
        return variables["out"]



def main():
    simulator = CircuitSimulator("examples/gates.hdl")
    inputs = {"a": 1, "b": 0}
    # inputs = {"a": 0}
    outputs = simulator.evaluate("And", inputs)
    print(outputs)

if __name__ == "__main__":
    main()
        

        

        


