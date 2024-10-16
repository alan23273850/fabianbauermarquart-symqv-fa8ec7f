#!/bin/bash

for n in {95..99}; do
    echo "Running BVsingle.py on circuit $n"
    timeout 300 ./BVsingle.py ~/AutoQ/benchmark_ver/flip/BV/$n/circuit.qasm
done

echo "Running GHZsingle.py on circuit 064"
timeout 300 ./GHZsingle.py ~/AutoQ/benchmark_ver/flip/GHZzero/064/circuit.qasm
for (( n=128; n<=512; n=n+128 )); do
    echo "Running GHZsingle.py on circuit $n"
    timeout 300 ./GHZsingle.py ~/AutoQ/benchmark_ver/flip/GHZzero/$n/circuit.qasm
done

for (( n=8; n<=128; n=n*2 )); do
    echo "Running GHZall.py on circuit $n"
    timeout 300 ./GHZall.py ~/AutoQ/benchmark_ver/flip/GHZall/$(printf "%03d" $n)/circuit.qasm
done

for (( n=12; n<=20; n=n+2 )); do
    echo "Running GroverSingle.py on circuit $n"
    timeout 300 ./GroverSingle.py ~/AutoQ/benchmark_ver/flip/Grover/$n/circuit.qasm
done

for (( n=6; n<=10; n=n+1 )); do
    echo "Running GroverAll.py on circuit $n"
    timeout 300 ./GroverAll.py ~/AutoQ/benchmark_ver/flip/MOGrover/$(printf "%02d" $n)/circuit.qasm
done

for (( n=8; n<=16; n=n+2 )); do
    echo "Running MCXall.py on circuit $n"
    timeout 300 ./MCXall.py ~/AutoQ/benchmark_ver/flip/MCToffoli/$(printf "%02d" $n)/circuit.qasm
done
