#!/usr/bin/python3
import sys; sys.path.append('../..')
import read_qasm
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.expressions.qbit import QbitVal
from symqv.lib.expressions.complex import ComplexVal
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import CNOT, CCX
from z3 import And, Not, Or

def prove_MCXall(filename: str):
    circuit = read_qasm.read_qasm(filename)
    q = len(circuit.qbits)

    initial_values = [{(1, 0), (0, 1)}]
    for i in range(1, q):
        if i % 2 == 1:
            initial_values.append({(1, 0), (0, 1)})
        else:
            initial_values.append((1, 0))
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    final_qbits = circuit.get_final_qbits()
    conjunction = [Or(final_qbits[0].isclose(QbitVal(alpha = ComplexVal(1), beta = ComplexVal(0)), circuit.delta),
                      final_qbits[0].isclose(QbitVal(alpha = ComplexVal(0), beta = ComplexVal(1)), circuit.delta))]
    for i in range(1, q):
        if i % 2 == 1:
            conjunction.append(Or(final_qbits[i].isclose(QbitVal(alpha = ComplexVal(1), beta = ComplexVal(0)), circuit.delta),
                                  final_qbits[i].isclose(QbitVal(alpha = ComplexVal(0), beta = ComplexVal(1)), circuit.delta)))
        else:
            conjunction.append(final_qbits[i].isclose(QbitVal(alpha = ComplexVal(1), beta = ComplexVal(0)), circuit.delta))
    circuit.solver.add(Not(And(conjunction)))

    # Prove
    print(circuit.prove(method=Method.qbit_sequence_model))#, dump_smt_encoding=True, dump_solver_output=True))
    # have bugs when n = 1 !
    # The output model (counterexample) is
    # 'q0_final.alpha.r': 0,
    # 'q0_final.alpha.i': 0,
    # 'q0_final.beta.r': 0,
    # 'q0_final.beta.i': -1,
    # 'q1_final.alpha.r': 0,
    # 'q1_final.alpha.i': 0,
    # 'q1_final.beta.r': 0,
    # 'q1_final.beta.i': 1,
    # but the imaginary parts should be zero!

if __name__ == "__main__":
    prove_MCXall(sys.argv[1])
# ./MCXall.py ~/AutoQ/benchmark_ver/flip/MCToffoli/08/circuit.qasm
