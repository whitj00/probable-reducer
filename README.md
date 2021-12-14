## Probablistic Reducer Functions for Rainbow Tables using Markovian Dictionaries

A loose implementation of Arvind Narayanan and Vitaly Shmatikov's [Fast Dictionary Attacks on Passwords Using Time-Space Tradeoff](https://www.cs.utexas.edu/~shmat/shmat_ccs05pwd.pdf).

Individual letter frequencies are generated from the *_Concise Oxford Dictionary_* (9th edition, 1995) by Barry Keating and available [here](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html).

Bigram frequencies are from [English Letter Frequency Counts: Mayzner Revisited](http://norvig.com/mayzner.html) by Peter Norvig. The code to extract frequencies is available [here](https://gist.github.com/lydell/c439049abac2c9226e53/).

For fastest results, use [pypy](https://www.pypy.org).