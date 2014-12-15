#!/bin/bash
echo Trial 1
date
python shortest_path_tests.py -V 100 -E 500 -t 20 > speed_v_100_e500.txt
echo Trial 2
date
python shortest_path_tests.py -V 100 -E 1000 -t 20 > speed_v_100_e1000.txt
echo Trial 3
date
python shortest_path_tests.py -V 100 -E 2000 -t 20 > speed_v_100_e1000.txt
echo Trial 4
date
python shortest_path_tests.py -V 100 -E 5000 -t 20 > speed_v_100_e5000.txt
echo Trial 5
date
python shortest_path_tests.py -V 1000 -E 5000 -t 20 > speed_v_1000_e10000.txt
echo Trial 6
date
python shortest_path_tests.py -V 1000 -E 10000 -t 20 > speed_v_1000_e10000.txt
echo Trial 7
date
python shortest_path_tests.py -V 1000 -E 20000 -t 20 > speed_v_1000_e20000.txt
echo Trial 8
date
python shortest_path_tests.py -V 1000 -E 50000 -t 20 > speed_v_1000_e50000.txt


