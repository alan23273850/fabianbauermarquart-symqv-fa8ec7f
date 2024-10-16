#!/usr/bin/python3
import sys; sys.path.append('../..')
import read_qasm
from math import sqrt
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import H, CNOT
from symqv.lib.solver import SpecificationType

def prove_GHZsingle(filename: str):
    circuit = read_qasm.read_qasm(filename)
    q = len(circuit.qbits)
    initial_values = [(1, 0) for _ in range(q)]
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    circuit.set_specification([1/sqrt(2)] + [0 for _ in range((1 << q) - 2)] + [1/sqrt(2)], SpecificationType.final_state_vector)

    # Prove
    print(circuit.prove(method=Method.state_model))#, dump_solver_output = True))


if __name__ == "__main__":
    prove_GHZsingle(sys.argv[1])
# ./GHZsingle.py ~/AutoQ/benchmark_ver/flip/GHZzero/064/circuit.qasm
