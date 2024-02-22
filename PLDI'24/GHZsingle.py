#!/usr/bin/python3
import sys; sys.path.append('..')
import time
import numpy as np
from math import sqrt
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import H, CNOT
from symqv.lib.solver import SpecificationType

def prove_GHZsingle(q: int):
    qbits = Qbits([f'q{i}' for i in range(q)])
    circuit = Circuit(qbits,
                        [H(qbits[0])] +
                        [CNOT(qbits[i-1], qbits[i]) for i in range(1, q)])
                    #   , delta=0.0001)
    print(circuit)
    initial_values = [(1, 0) for _ in range(q)]
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    circuit.set_specification([1/sqrt(2)] + [0] * (2 ** q - 2) + [1/sqrt(2)], SpecificationType.final_state_vector)

    # Prove
    print(circuit.prove(method=Method.state_model))#, dump_solver_output = True))


if __name__ == "__main__":
    times = []

    for _ in range(1):
        start = time.time()
        prove_GHZsingle(int(sys.argv[1]))
        times.append(time.time() - start)

    print(f'Runtime:', np.mean(times))
