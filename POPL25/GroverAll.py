#!/usr/bin/python3
import sys; sys.path.append('../..')
import read_qasm
from math import pi, asin, sqrt
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import X, H, CNOT, CCX, CZ
from symqv.lib.solver import SpecificationType

aH = {3: 11 / pow(sqrt(2), 7), 6: 133988401 / pow(2, 27), 7: 12412280691169 / pow(sqrt(2), 87), 8: 75555863006653472909761 / pow(2, 76), 9: -15034347071300495523371427226121933183 / pow(sqrt(2), 247), 10: -51408163609015342607074675483845466135738782582421858486334207 / pow(2, 205)}
aL = {3: -1 / pow(sqrt(2), 7), 6: -988079 / pow(2, 27), 7: 73054448161 / pow(sqrt(2), 87), 8: 34433006489313897025 / pow(2, 76), 9: -15629794375924256137689018495406207 / pow(sqrt(2), 247), 10: 37317028493000746132194989664756306857260930471704364830465 / pow(2, 205)}

def prove_GroverAll(filename: str):
    circuit = read_qasm.read_qasm(filename)
    q = len(circuit.qbits); n = q // 3
    initial_values = [{(1, 0), (0, 1)} for _ in range(n)]
    initial_values.extend([(1, 0) for _ in range(n, q)])
    circuit.initialize(initial_values)
    # circuit.execute(True)

    # Build specification
    nonzero_indices = []
    for i in range(1 << n):
        t = 0
        for _ in range(n):
            t <<= 1
            t += i & 1
            i >>= 1
        a = t & 1
        a <<= 1
        t >>= 1
        for _ in range(2, n+1):
            a += t & 1
            a <<= 2
            t >>= 1
        a += 1
        nonzero_indices.append(a)
    #############################
    possible_final_state_vectors = []
    final_state_vector_backup = [0 for _ in range(1 << q)]
    for s in range(1 << n):
        final_state_vector = final_state_vector_backup
        base = s << (q-n)
        for i, num in enumerate(nonzero_indices):
            if i == s:
                final_state_vector[base + num] = aH[n] #Complex('aH')
            else:
                final_state_vector[base + num] = aL[n] #Complex('aL')
        possible_final_state_vectors.append(final_state_vector.copy()) # .copy() is IMPORTANT !!!
    circuit.set_specification(possible_final_state_vectors, SpecificationType.possible_final_state_vectors)
    # circuit.solver.add(Complex('aH').r * Complex('aH').r > Complex('aL').r * Complex('aL').r)
    # circuit.solver.add(And(-circuit.delta <= Complex('aH').i, Complex('aH').i <= circuit.delta))
    # circuit.solver.add(And(-circuit.delta <= Complex('aL').i, Complex('aL').i <= circuit.delta))

    # Prove
    print(circuit.prove(method=Method.state_model))#, dump_solver_output = True))


if __name__ == "__main__":
    prove_GroverAll(sys.argv[1])
# ./GroverAll.py ~/AutoQ/benchmark_ver/flip/MOGrover/06/circuit.qasm
