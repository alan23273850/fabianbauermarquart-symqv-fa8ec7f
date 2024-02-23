#!/usr/bin/python3
import sys; sys.path.append('..')
import time
import numpy as np
from math import sqrt
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import H, CNOT
from symqv.lib.solver import SpecificationType

def prove_GHZall(q: int):
    qbits = Qbits([f'q{i}' for i in range(q)])
    circuit = Circuit(qbits,
                        [H(qbits[0])] +
                        [CNOT(qbits[i-1], qbits[i]) for i in range(1, q)])
                    #   , delta=0.0001)
    print(circuit)
    initial_values = [{(1, 0), (0, 1)} for _ in range(q)]
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    possible_final_state_vectors = []
    final_state_vector = [0] * (2 ** q)
    for i in range(2 ** (q-1)):
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
    times = []

    for _ in range(1):
        start = time.time()
        prove_GHZall(int(sys.argv[1]))
        times.append(time.time() - start)

    print(f'Runtime:', np.mean(times))
