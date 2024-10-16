#!/usr/bin/python3
import sys; sys.path.append('../..')
import read_qasm
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.expressions.qbit import QbitVal
from symqv.lib.expressions.complex import ComplexVal
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import H, Z, CCX
from z3 import And, Not, Or

def prove_BVall(filename: str):
    circuit = read_qasm.read_qasm(filename)
    q = len(circuit.qbits); n = (q-1) // 2

    initial_values = []
    for i in range(q):
        if i % 2 == 0 and i < q-1:
            initial_values.append({(1, 0), (0, 1)})
        else:
            initial_values.append((1, 0))
    # print(initial_values)
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    final_qbits = circuit.get_final_qbits()
    conjunction = []
    for i in range(n):
        if i % 2 == 0:
            conjunction.append(Or(final_qbits[i].isclose(QbitVal(alpha = ComplexVal(1), beta = ComplexVal(0)), circuit.delta),
                                  final_qbits[i].isclose(QbitVal(alpha = ComplexVal(0), beta = ComplexVal(1)), circuit.delta)))
        else:
            conjunction.append(final_qbits[i].isclose(final_qbits[i-1], circuit.delta))
    conjunction.append(final_qbits[-1].isclose(QbitVal(alpha = ComplexVal(0), beta = ComplexVal(1)), circuit.delta))
    circuit.solver.add(Not(And(conjunction)))

    # Prove
    print(circuit.prove(method=Method.qbit_sequence_model))


if __name__ == "__main__":
    prove_BVall(sys.argv[1])
# ./BVall.py ~/AutoQ/benchmark_ver/gm/MOBV_reorder/09/circuit.qasm
