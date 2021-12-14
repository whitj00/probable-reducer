While we recommend using PyPy3 to run the program with a significant speedup, the CPython3 interpreter will work as well. Our project should have no external dependencies to install.

Our program will create Markovian dictionaries and Rainbow Tables according to specified password parameters and crack up to 500 passwords from a specified hash file. The `-c` parameter specifies the target number of chains. The `-l` parameter specifies the length of each chain. Using `-o 0` will use a zero-order Markov reducer, using `-o 1` will use a first-order Markov reducer, and using `--conventional` will use a conventional reducer. `-pl` will set the fixed-length of passwords our reducer should produce. `-i` will specify the path of an input file. By default, our program will use a length of 6 and attempt to decrypt the 6 letter-RockYou passwords in the `data/` directory. Cracked passwords are printed in `cracked.txt` and to the console.

For instance, we can run our zero-order model with 4000 chains of length 75 with the command `pypy3 crack.py -o 0 -c 4000 -l 75`. This will produce a console output that starts like the following:

```
root@ubuntu-c-2-4gib-sfo3-01:~/probable-reducer# pypy3 crack.py -o 0 -c 4000 -l 75
Created a order 0 markov dictionary of size 597539 [Time: 0.012989044189453125s]
Collision Rate: 0.19825000000000004
Encoded Passwords: 240525
000ea5be968306934418b610e33e35b6:leilen [Success Rate: 0.76% (1/132)]
00112c782c3bed8f75a220e5ba0dcac5:eimeel [Success Rate: 1.39% (2/144)]
0016bb0668ac0f17aa5cbe844b6df4f6:pearse [Success Rate: 1.56% (3/192)]
```