#!/usr/bin/python3
import sys; sys.path.append('../..')
import read_qasm
from math import sqrt
from symqv.lib.models.circuit import Method
from symqv.lib.solver import SpecificationType

def prove_GHZall(filename: str):
    circuit = read_qasm.read_qasm(filename)
    q = len(circuit.qbits)
    initial_values = [{(1, 0), (0, 1)} for _ in range(q)]
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    possible_final_state_vectors = []
    final_state_vector = [0 for _ in range(1 << q)]
    for i in range(1 << (q-1)):
        final_state_vector[i] = 1.0 / sqrt(2)
        final_state_vector[2**q-1 - i] = 1.0 / sqrt(2)
        possible_final_state_vectors.append(final_state_vector.copy()) # .copy() is IMPORTANT !!!
        final_state_vector[2**q-1 - i] = -1.0 / sqrt(2)
        possible_final_state_vectors.append(final_state_vector.copy()) # .copy() is IMPORTANT !!!
        final_state_vector[i] = 0
        final_state_vector[2**q-1 - i] = 0
    circuit.set_specification(possible_final_state_vectors, SpecificationType.possible_final_state_vectors)

    # Prove
    print(circuit.prove(method=Method.state_model))#, dump_solver_output = True))


if __name__ == "__main__":
    prove_GHZall(sys.argv[1])
# ./GHZall.py ~/AutoQ/benchmark_ver/flip/GHZall/008/circuit.qasm
