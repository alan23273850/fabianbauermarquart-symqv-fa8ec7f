#!/usr/bin/python3
import sys; sys.path.append('../..')
import read_qasm
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.expressions.qbit import QbitVal
from symqv.lib.expressions.complex import ComplexVal
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import H
from z3 import And, Not, Or

def prove_H2all(filename: str):
    circuit = read_qasm.read_qasm(filename)
    q = len(circuit.qbits)

    initial_values = [{(1, 0), (0, 1)} for _ in range(q)]
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
    print(circuit.prove(method=Method.qbit_sequence_model))#, dump_smt_encoding=True, dump_solver_output=True))


if __name__ == "__main__":
    prove_H2all(sys.argv[1])
# ./H2all.py ~/AutoQ/benchmark_ver/gm/H2/012/circuit.qasm