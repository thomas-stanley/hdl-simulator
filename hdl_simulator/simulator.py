from .parser import HDLParser

class CircuitSimulator:
    def __init__(self, filename):
        # Parses the HDL file and initialises the simulator with the parsed modules
        parser = HDLParser()
        self.modules = {module.name: module for module in parser.parse(filename)}  # Parsed modules stored here

    def evaluate(self, module_name, inputs):
        # Evaluates a module given its name and inputs
        if module_name == "Nand":
            if len(inputs) != 2:
                raise ValueError(f"Expected 2 inputs for '{module_name}' module, got {len(inputs)}.")
            return {"out": int(not(inputs["a"] and inputs["b"]))}

        if module_name not in self.modules:  # Checks if module is valid (no need to also check if it's nand as that was done earlier)
            raise ValueError(f"Module '{module_name}' not found.")
        
        self._validate_inputs(inputs, module_name)
        
        return self.evaluate_module(module_name, inputs)


    def _validate_inputs(self, inputs, module_name):
        if not all(isinstance(input_value, int) for input_value in inputs.values()):  # Checks if inputs are integers
            raise TypeError("Inputs must be integers.")

        if not all(input_value in (0, 1) for input_value in inputs.values()):  # Checks if inputs are 0 or 1
            raise ValueError("Inputs must be either 0 or 1.")
    
    
    def evaluate_module(self, module_name, inputs):

        module = self.modules[module_name]
        module_inputs = module.inputs
        module_outputs = module.outputs
        variables = inputs.copy()

        if len(inputs) != len(module_inputs):  # Checks if there are the correct number of inputs
            raise ValueError(f"Expected {module_inputs} for '{module.name}', got {len(inputs)}.")

        for variable, expression in module.body:
            function = expression["module"]
            arguments = expression["args"]

            if all(arg in variables for arg in arguments):  # If the function can be calculated with the known variables (initially the variables specified by the user)
                if function == "Nand":
                    variables[variable] = int(not (variables[arguments[0]] and variables[arguments[1]]))  # Calculates the nand gate for the current variable in the queue
                else:
                    sub_inputs = {module_inputs[arg_index]: variables[arg] for arg_index, arg in enumerate(arguments)}  # Stores relevant arguments for the submodule with the correct name for the submodule that will be called
                    sub_outputs = self.evaluate_module(function, sub_inputs)  # Run the evaluation on the submodule
                    to_add = {variable: output_value for output_value in tuple(sub_outputs.values())}  # Reassigns correct output variable names
                
                    variables.update(to_add)  # Add the submodule output to the found variables
        return {out: variables[out] for out in module_outputs}                          



def main():
    test_simulator = CircuitSimulator("examples/gates.hdl")
    inputs = {"a": 0, "b": 1}
    outputs = test_simulator.evaluate("Or", inputs)
    print(outputs)
        

        

        


