import csv
from string import ascii_lowercase as ascii_letters
from math import log as ln

occurences = {letter: {letter_:1 for letter_ in ascii_letters} for letter in ascii_letters}
frequencies = {letter: {} for letter in ascii_letters}

with open("data/words.txt", 'r') as file:
    for line in file:
        line = line.strip()
        for i in range(len(line)-1):
            occurences[line[i]][line[i+1]] += 1

min_freq = 0

for letter in ascii_letters:
    total = sum(map(int,occurences[letter].values()))
    for letter_ in ascii_letters:
        freq = occurences[letter][letter_]/total
        log_freq = ln(freq)
        frequencies[letter][letter_] = log_freq
        min_freq = min(min_freq, log_freq)

scale_value = -1000/min_freq

with open('data/bigram.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for letter in ascii_letters:
        for letter_ in ascii_letters:
            freq = frequencies[letter][letter_] * scale_value
            round_freq = round(freq)
            writer.writerow([letter, letter_, round_freq])

print(min_freq)