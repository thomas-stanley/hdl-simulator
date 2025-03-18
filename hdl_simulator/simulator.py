from .parser import parse_hdl

class CircuitSimulator:
    def __init__(self, filename):
        # Parses the HDL file and initialises the simulator with the parsed modules
        self.modules = {module.name: module for module in parse_hdl(filename)}  # Parsed modules stored here

    def evaluate(self, module_name, inputs):
        # Evaluates a module given its name and inputs
        if module_name == "Nand":
            if len(inputs) != 2:
                raise ValueError(f"Expected 2 inputs for {module_name} module, got {len(inputs)}.")
            return {"out": int(not(inputs["a"] and inputs["b"]))}

        if module_name not in self.modules:
            raise ValueError(f"Module {module_name} not found.")
        
        return self.evaluate_module(module_name, inputs)
    
    def evaluate_module(self, module_name, inputs):

        module = self.modules[module_name]
        logic = module.body
        variables = inputs.copy()

        queue = list(logic)

        while queue:  # While there are still unresolved expressions
            remaining_queue = []  # Unresolved expressions

            for variable, expression in queue:
                function = expression["module"]
                arguments = expression["args"]

                if all(arg in variables for arg in arguments):  # If the function can be calculated with the known variables (initially the variables specified by the user)
                    if function == "Nand":
                        variables[variable] = int(not (variables[arguments[0]] and variables[arguments[1]]))  # Calculates the nand gate for the current variable in the queue
                    else:
                        alphabet = "abcdefghijklmnopqrstuvwxyz"  # jerry rigged way to fix issue with arguments and variable mismatch
                        sub_inputs = {alphabet[arg_index]: variables[arg] for arg_index, arg in enumerate(arguments)}  # Stores relevant arguments for the submodule
                        sub_outputs = self.evaluate_module(function, sub_inputs)  # Run the evaluation on the submodule
                        variables.update(sub_outputs)  # Add the submodule output to the found variables
            queue = []
            """
                else:
                    remaining_queue.append(variable, expression)
            """
        return {out: variables[out] for out in module.outputs}                          



def main():
    test_simulator = CircuitSimulator("examples/gates.hdl")
    inputs = {"a": 0, "b": 0}
    # inputs = {"a": 0}
    outputs = test_simulator.evaluate("And", inputs)  # Need to write some tests for this to speed up debugging
    print(outputs)
        

        

        


