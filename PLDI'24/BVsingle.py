#!/usr/bin/python3
import sys; sys.path.append('..')
import time
import numpy as np
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.expressions.qbit import QbitVal
from symqv.lib.expressions.complex import ComplexVal
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import H, Z, CNOT
from z3 import And, Not

def prove_BVsingle(n: int):
    q = n+1
    qbits = Qbits([f'q{i}' for i in range(q)])
    circuit = Circuit(qbits,
                        [H(qbit) for qbit in qbits] +
                        [Z(qbits[-1])] +
                        [CNOT(qbit, qbits[-1]) for i, qbit in enumerate(qbits) if i % 2 == 0 and i < len(qbits)-1] +
                        [H(qbit) for qbit in qbits])
                    #   , delta=0.0001)
    print(circuit)
    initial_values = [(1, 0) for _ in range(q)]
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    final_qbits = circuit.get_final_qbits()
    conjunction = []
    for i in range(n):
        conjunction.append(final_qbits[i].isclose(QbitVal(alpha = ComplexVal(i % 2), beta = ComplexVal(1 - (i % 2))), circuit.delta))
    conjunction.append(final_qbits[-1].isclose(QbitVal(alpha = ComplexVal(0), beta = ComplexVal(1)), circuit.delta))
    circuit.solver.add(Not(And(conjunction)))

    # Prove
    print(circuit.prove(method=Method.qbit_sequence_model))#, dump_smt_encoding=True, dump_solver_output=True))
    # The bug appears here! The result differs when n = 1.
    # Method.qbit_sequence_model => UNSAT, Method.state_model => SAT


if __name__ == "__main__":
    times = []

    for _ in range(1):
        start = time.time()
        prove_BVsingle(int(sys.argv[1]))
        times.append(time.time() - start)

    print(f'Runtime:', np.mean(times))
