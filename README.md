## Probablistic Reducer Functions for Rainbow Tables using Markovian Dictionaries

A loose implementation of Arvind Narayanan and Vitaly Shmatikov's [Fast Dictionary Attacks on Passwords Using Time-Space Tradeoff](https://www.cs.utexas.edu/~shmat/shmat_ccs05pwd.pdf).

Individual letter frequencies are generated from the *_Concise Oxford Dictionary_* (9th edition, 1995) by Barry Keating and available [here](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html).

Words are from https://github.com/dwyl/english-words

For fastest results, use [pypy](https://www.pypy.org).