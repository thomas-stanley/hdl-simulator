class Module:
    def __init__(self, name, inputs, outputs, body):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.body = body  # List of module logic expressions

    def __repr__(self):
        return f"Module({self.name}, inputs={self.inputs}, outputs={self.outputs})"
