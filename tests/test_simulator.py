import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hdl_simulator import CircuitSimulator, parse_hdl

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