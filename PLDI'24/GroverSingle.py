#!/usr/bin/python3
import sys; sys.path.append('..')
import time
import numpy as np
from math import pi, asin, sqrt
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.models.circuit import Circuit, Method
from symqv.lib.operations.gates import X, H, CNOT, CCX, CZ
from symqv.lib.solver import SpecificationType
from symqv.lib.expressions.complex import Complex
from z3 import And

aH = {3: 11 / pow(sqrt(2), 7)}
aL = {3: -1 / pow(sqrt(2), 7)}

def one_iteration(qbits, n: int, q: int):
    ans = []
    ans.append(X(qbits[0]))
    ans.extend([X(qbits[i]) for i in range(3, q-1, 4)])
    assert(n >= 3)
    if n >= 3:
        temp = []
        for t in range(2, q, 2):
            temp.append(CCX(qbits[t-2], qbits[t-1], qbits[t]))
        ans.extend(temp)
        ans.append(CNOT(qbits[-2], qbits[-1]))
        ans.extend(list(reversed(temp)))
    else:
        assert(n == 2)
        sys.exit()
        # aut.Toffoli(3, 4, 5);
    ans.append(X(qbits[0]))
    ans.extend([X(qbits[i]) for i in range(3, q-1, 4)])
    ans.append(H(qbits[0]))
    ans.extend([H(qbits[2*i-1]) for i in range(1, n)])
    ans.append(X(qbits[0]))
    ans.extend([X(qbits[2*i-1]) for i in range(1, n)])
    if n >= 3:
        temp = []
        for t in range(2, q-2, 2):
            temp.append(CCX(qbits[t-2], qbits[t-1], qbits[t]))
        ans.extend(temp)
        ans.append(CZ(qbits[2*n-4], qbits[2*n-3]))
        ans.extend(list(reversed(temp)))
    else:
        assert(n == 2)
        sys.exit()
        # aut.CZ(3, 4);
    ans.append(X(qbits[0]))
    ans.extend([X(qbits[2*i-1]) for i in range(1, n)])
    ans.append(H(qbits[0]))
    ans.extend([H(qbits[2*i-1]) for i in range(1, n)])
    return ans

def prove_GroverSingle(n: int):
    q = 2 * n
    qbits = Qbits([f'q{i}' for i in range(q)])
    circuit = Circuit(qbits,
                        [X(qbits[-1])] +
                        [H(qbits[0])] + [H(qbits[i]) for i in range(1, q, 2)] +
                        one_iteration(qbits, n, q) * int(pi / (4 * asin(1 / pow(2, n/2.0)))) +
                        [H(qbits[-1])])
                    #   , delta=0.0001)
    print(circuit)
    initial_values = [(1, 0) for _ in range(q)]
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
    final_state_vector = [0] * (1 << q)
    s = 0
    for i in range(n):
        s <<= 1
        s += i % 2
    for i, num in enumerate(nonzero_indices):
        if i == s:
            final_state_vector[num] = aH[n] #Complex('aH')
        else:
            final_state_vector[num] = aL[n] #Complex('aL')
    circuit.set_specification(final_state_vector, SpecificationType.final_state_vector)
    # circuit.solver.add(Complex('aH').r * Complex('aH').r > Complex('aL').r * Complex('aL').r)
    # circuit.solver.add(And(-circuit.delta <= Complex('aH').i, Complex('aH').i <= circuit.delta))
    # circuit.solver.add(And(-circuit.delta <= Complex('aL').i, Complex('aL').i <= circuit.delta))

    # Prove
    print(circuit.prove(method=Method.state_model))#, dump_solver_output = True))


if __name__ == "__main__":
    times = []

    for _ in range(1):
        start = time.time()
        prove_GroverSingle(int(sys.argv[1]))
        times.append(time.time() - start)

    print(f'Runtime:', np.mean(times))
