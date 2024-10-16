import re, subprocess
import sys; sys.path.insert(0, '..')
from symqv.lib.expressions.qbit import Qbits
from symqv.lib.models.circuit import Circuit
from symqv.lib.operations.gates import X, H, Z, CCX, CNOT, CZ

def read_qasm(filename: str) -> Circuit:
    with open(filename, 'r') as file:
        lines = file.readlines()
    qbits = Qbits([])
    gate_list = []
    for line in lines:
        line = line.strip()
        if line.startswith("//") or not line:
            continue
        match = re.compile(r' *qreg .*\[(\d+)\]').match(line)
        if match:
            q = int(match.group(1))
            assert q == int(subprocess.run(f'grep -Po ".*qreg.*\[\K\d+(?=\];)" {filename}', shell=True, capture_output=True, executable='/bin/bash').stdout.splitlines()[0].decode('utf-8'))
            qbits = Qbits([f'q{i}' for i in range(q)])
        else:
            match = re.compile(r' *h .*\[(\d+)\]').match(line) # h qubits[0];
            if match:
                gate_list.append(H(qbits[int(match.group(1))]))
            match = re.compile(r' *z .*\[(\d+)\]').match(line)
            if match:
                gate_list.append(Z(qbits[int(match.group(1))]))
            match = re.compile(r' *x .*\[(\d+)\]').match(line)
            if match:
                gate_list.append(X(qbits[int(match.group(1))]))
            match = re.compile(r' *ccx .*\[(\d+)\].*\[(\d+)\].*\[(\d+)\]').match(line)
            if match:
                gate_list.append(CCX(qbits[int(match.group(1))], qbits[int(match.group(2))], qbits[int(match.group(3))]))
            match = re.compile(r' *cx .*\[(\d+)\].*\[(\d+)\]').match(line)
            if match:
                gate_list.append(CNOT(qbits[int(match.group(1))], qbits[int(match.group(2))]))
            match = re.compile(r' *cz .*\[(\d+)\].*\[(\d+)\]').match(line)
            if match:
                gate_list.append(CZ(qbits[int(match.group(1))], qbits[int(match.group(2))]))
    assert len(gate_list) == int(subprocess.run(f'grep -P ".*(x |y |z |h |s |t |rx\(.+\) |ry\(.+\) |cx |cz |ccx |tdg |sdg |swap ).*\[\d+\];" {filename} | wc -l', shell=True, capture_output=True, executable='/bin/bash').stdout.splitlines()[0].decode('utf-8'))
    circuit = Circuit(qbits, gate_list)
                    #   , delta=0.0001)
    return circuit
