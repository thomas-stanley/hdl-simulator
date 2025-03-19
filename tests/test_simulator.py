import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hdl_simulator import CircuitSimulator

@pytest.fixture(scope="module")
def simulator():  # So I only have to create an instance once
    return CircuitSimulator("examples/gates.hdl")

@pytest.mark.parametrize("a, b, expected", 
                         [(0, 0, 1), 
                          (0, 1, 1), 
                          (1, 0, 1), 
                          (1, 1, 0)])
def test_nand(simulator, a, b, expected):
    result = simulator.evaluate("Nand", {"a": a, "b": b})
    assert result["out"] == expected


@pytest.mark.parametrize("a, b, expected", 
                         [(0, 0, 0), 
                          (0, 1, 0), 
                          (1, 0, 0), 
                          (1, 1, 1)])
def test_and(simulator, a, b, expected):
    result = simulator.evaluate("And", {"a": a, "b": b})
    assert result["out"] == expected


@pytest.mark.parametrize("a, b, expected", 
                         [(0, 0, 0), 
                          (0, 1, 1), 
                          (1, 0, 1), 
                          (1, 1, 1)])
def test_or(simulator, a, b, expected):
    result = simulator.evaluate("Or", {"a": a, "b": b})
    assert result["out"] == expected


@pytest.mark.parametrize("a, expected", 
                         [(0, 1), 
                          (1, 0)])
def test_not(simulator, a, expected):
    result = simulator.evaluate("Not", {"a": a})
    assert result["out"] == expected


@pytest.mark.parametrize("a, b, expected", 
                         [(0, 0, 0), 
                          (0, 1, 1), 
                          (1, 0, 1), 
                          (1, 1, 0)])
def test_xor(simulator, a, b, expected):
    result = simulator.evaluate("Xor", {"a": a, "b": b})
    assert result["out"] == expected


@pytest.mark.parametrize("inputs", 
                         [{},  # Missing both inputs
                          {"a": 0},  # Missing one input
                          {"a": 0, "b": 0, "c": 0}])  # Extra input
def test_nand_input_validation(simulator, inputs):
    with pytest.raises(ValueError):
        simulator.evaluate("Nand", inputs)


@pytest.mark.parametrize("inputs",
                         [{},  # Missing input
                          {"a": 0, "b": 0}])  # Extra input
def test_not_input_validation(simulator, inputs):
    with pytest.raises(ValueError):
        simulator.evaluate("Not", inputs)


@pytest.mark.parametrize("module, inputs, error_type",
                         [("And", {"a": "string_1", "b": "string_2"}, TypeError),
                          ("Or", {"a": 1.5, "b": 0.5}, TypeError),
                          ("Xor", {"a": -1, "b": -2}, ValueError),
                          ("And", {"a": 2, "b": 1}, ValueError)])
def test_erroneous_input(simulator, module, inputs, error_type):
    with pytest.raises(error_type):
        simulator.evaluate(module, inputs)


def test_unknown_module(simulator):
    with pytest.raises(ValueError, match="Module 'InvalidModule' not found."):
        simulator.evaluate("InvalidModule", {"a": 0, "b": 0})


