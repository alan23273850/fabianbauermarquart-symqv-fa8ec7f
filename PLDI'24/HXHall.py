#!/usr/bin/python3
import sys; sys.path.append('..')
import time
import numpy as np
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.expressions.qbit import QbitVal
from symqv.lib.expressions.complex import ComplexVal
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import H, X
from z3 import And, Not, Or

def prove_HXHall(q: int):
    qbits = Qbits([f'q{i}' for i in range(q)])
    circuit = Circuit(qbits,
                        [H(qbit) for qbit in qbits] +
                        [X(qbit) for qbit in qbits] +
                        [H(qbit) for qbit in qbits])
                    #   , delta=0.0001)
    print(circuit)
    initial_values = [{(1, 0), (0, 1)} for _ in range(q)]
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    final_qbits = circuit.get_final_qbits()
    conjunction = []
    for i in range(q):
        conjunction.append(Or(final_qbits[i].isclose(QbitVal(alpha = ComplexVal(1), beta = ComplexVal(0)), circuit.delta),
                              final_qbits[i].isclose(QbitVal(alpha = ComplexVal(0), beta = ComplexVal(-1)), circuit.delta)))
    circuit.solver.add(Not(And(conjunction)))

    # Prove
    print(circuit.prove(method=Method.qbit_sequence_model))#, dump_smt_encoding=True, dump_solver_output=True))


if __name__ == "__main__":
    times = []

    for _ in range(1):
        start = time.time()
        prove_HXHall(int(sys.argv[1]))
        times.append(time.time() - start)

    print(f'Runtime:', np.mean(times))
