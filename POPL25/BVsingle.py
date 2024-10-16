#!/usr/bin/python3
import sys; sys.path.append('../..')
import read_qasm
from symqv.lib.expressions.qbit import QbitVal
from symqv.lib.expressions.complex import ComplexVal
from symqv.lib.models.circuit import Method
from z3 import And, Not

def prove_BVsingle(filename: str):
    circuit = read_qasm.read_qasm(filename)
    n = len(circuit.qbits) - 1

    initial_values = [(1, 0) for _ in range(len(circuit.qbits))]
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
    prove_BVsingle(sys.argv[1])
# ./BVsingle.py ~/AutoQ/benchmark_ver/flip/BV/95/circuit.qasm
