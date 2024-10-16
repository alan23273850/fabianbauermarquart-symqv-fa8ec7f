#!/bin/bash

# for n in {95..99}; do
#     echo "Running BVsingle.py on circuit $n"
#     timeout 300 ./BVsingle.py ~/AutoQ/benchmark_ver/gm/BV/$n/circuit.qasm
# done

# for n in {09..13}; do
#     echo "Running BVall.py on circuit $n"
#     timeout 300 ./BVall.py ~/AutoQ/benchmark_ver/gm/MOBV_reorder/$n/circuit.qasm
# done

# echo "Running GHZsingle.py on circuit 064"
# timeout 300 ./GHZsingle.py ~/AutoQ/benchmark_ver/gm/GHZzero/064/circuit.qasm
# for (( n=128; n<=512; n=n+128 )); do
#     echo "Running GHZsingle.py on circuit $n"
#     timeout 300 ./GHZsingle.py ~/AutoQ/benchmark_ver/gm/GHZzero/$n/circuit.qasm
# done

# for (( n=8; n<=128; n=n*2 )); do
#     echo "Running GHZall.py on circuit $n"
#     timeout 300 ./GHZall.py ~/AutoQ/benchmark_ver/gm/GHZall/$(printf "%03d" $n)/circuit.qasm
# done

# for (( n=12; n<=20; n=n+2 )); do
#     echo "Running GroverSingle.py on circuit $n"
#     timeout 300 ./GroverSingle.py ~/AutoQ/benchmark_ver/gm/Grover/$n/circuit.qasm
# done

# for (( n=6; n<=10; n=n+1 )); do
#     echo "Running GroverAll.py on circuit $n"
#     timeout 300 ./GroverAll.py ~/AutoQ/benchmark_ver/gm/MOGrover/$(printf "%02d" $n)/circuit.qasm
# done

# for n in 012 013 064 128 256; do
#     echo "Running H2all.py on circuit $n"
#     timeout 300 ./H2all.py ~/AutoQ/benchmark_ver/gm/H2/$n/circuit.qasm
# done

# for n in 10 11 12 13 99; do
#     echo "Running HXHall.py on circuit $n"
#     timeout 300 ./HXHall.py ~/AutoQ/benchmark_ver/gm/HXH/$n/circuit.qasm
# done

# for (( n=8; n<=16; n=n+2 )); do
#     echo "Running MCXall.py on circuit $n"
#     timeout 300 ./MCXall.py ~/AutoQ/benchmark_ver/gm/MCToffoli/$(printf "%02d" $n)/circuit.qasm
# done

# for n in 02 18 50 75 100; do
for n in 02; do
    echo "Running OEGrover on circuit $n"
    timeout 300 time ./OEGrover.py ~/AutoQ/POPL25/Kick-the-Tires/non-parameterized/missgate/OEGrover/$n/circuit.qasm
done
