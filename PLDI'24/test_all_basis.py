#!/usr/bin/python3
import sys; sys.path.append('..')
import time
import numpy as np
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.expressions.qbit import QbitVal
from symqv.lib.expressions.complex import ComplexVal
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import H, X, Z
from z3 import And, Not, Or

def prove_all_basis():
    q = 1
    qbits = Qbits([f'q{i}' for i in range(q)])
    circuit = Circuit(qbits,
                        [H(qbits[0])] * 2 + [X(qbits[0])] * 3 + [Z(qbits[0])] * 2
                      )
                    #   , delta=0.0001)
    print(circuit)
    initial_values = []
    for i in range(q):
        initial_values.append({(1, 0), (0, 1)})

    print(initial_values)
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    final_qbits = circuit.get_final_qbits()
    conjunction = []
    for i in range(q):
        conjunction.append(Or(final_qbits[i].isclose(QbitVal(alpha = ComplexVal(1), beta = ComplexVal(0)), circuit.delta),
                              final_qbits[i].isclose(QbitVal(alpha = ComplexVal(0), beta = ComplexVal(1)), circuit.delta)))
    circuit.solver.add(Not(And(conjunction)))

    # Prove
    print(circuit.prove(method=Method.qbit_sequence_model))


if __name__ == "__main__":
    times = []

    for _ in range(1):
        start = time.time()
        prove_all_basis()
        times.append(time.time() - start)

    print(f'Runtime:', np.mean(times))
