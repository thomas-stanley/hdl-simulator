from parser import HDLParser

class CircuitSimulator:
    def __init__(self, filename):
        # Parses the HDL file and initialises the simulator with the parsed modules
        self.parser = HDLParser(filename)
        self.modules = self.parser.parse()  # Parsed modules stored here
    
