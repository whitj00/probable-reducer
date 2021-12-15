import time
from Reducer import Reducer
import string
import csv
from math import log as ln
from typing import Union

class FirstOrderMarkov(Reducer):

    def __init__(self, string_len : int) -> None:
        """Overrides reducer.__init__()"""
        self.string_len = string_len
        self.alphabet = list(string.ascii_lowercase)
        self.zero_order_prob_func = {'a': -247, 'b': -388, 'c': -309, 'd': -339, 'e': -219, 'f': -401, 'g': -370, 'h': -351, 'i': -258, 'j': -623, 'k': -451, 'l': -290, 'm': -350, 'n': -271, 'o': -264, 'p': -345, 'q': -623, 'r': -258, 's': -286, 't': -267, 'u': -332, 'v': -460, 'w': -435, 'x': -584, 'y': -403, 'z': -591}
        self.first_order_prob_func = self.__first_order_probabilities()
        self.threshold = -1350
        self.partial_size = {x:{letter:{} for letter in self.alphabet} for x in range(0,self.string_len+1)}
        self.partial_size[0]['*'] = {}
        self.size = self.__build_model()

    def __first_order_probabilities(self) -> dict:
        """Constructs probability dict for bi-grams"""
        prob_func = {letter:{} for letter in self.alphabet}
        with open('data/bigram.csv', 'r') as csvfile:
            bigram_reader = csv.reader(csvfile)
            for row in bigram_reader:
                prob_func[row[0]][row[1]] = int(row[2])
        return prob_func

    def __mu(self, first_char : str, second_char : str = None) -> Union[int, float]:
        """Returns log probability that `second_char` follows `first_char`"""
        if second_char is None:
            return self.zero_order_prob_func[first_char]
        return self.first_order_prob_func[first_char][second_char]


    def __partial_size2(self, current_length : int, prev_char : str, level : int) -> int:
        '''Partial size function for a first order Markov dictionary'''
        if level < self.threshold:
            self.partial_size[current_length][prev_char][level] = 0
            return 0
        if self.string_len == current_length:
            self.partial_size[current_length][prev_char][level] = 1
            return 1

        sum = 0
        for char in self.alphabet:
            if current_length == 0:
                new_level = self.__mu(char)
            else:
                new_level = level+self.__mu(prev_char,char)
            new_length = current_length+1
            if new_level in self.partial_size[new_length][char]:
                sum += self.partial_size[new_length][char][new_level]
            else:
                sum += self.__partial_size2(new_length,char,new_level)
        self.partial_size[current_length][prev_char][level] = sum

        return sum

    def __build_model(self) -> int:
        '''Builds our Markov dictionary'''
        return self.__partial_size2(0,'*',0)

    def __get_key2(self, current_length : int, index : int, prev_char : str, level : int) -> str:
        '''Helper function for get_key'''
        if self.string_len == current_length:
            return ""

        sum = 0
        for char in self.alphabet:
            if current_length == 0:
                new_level = self.__mu(char)
            else:
                new_level = level+self.__mu(prev_char,char)
            size = self.partial_size[current_length+1][char][new_level]
            if sum+size > index:
                return char + self.__get_key2(current_length+1, index-sum, char, new_level)
            sum = sum+size
        raise("index larger than keyspace size")

    def get_key(self, index : int) -> str:
        """Gets the i-th key in our Markov dictionary

        Args:
            index (int): Index of key in our Markov dictionary

        Returns:
            str: The i-th key in our Markov Dictionary
        """
        return self.__get_key2(0,index,'*',0)

    def reduce(self, index : int, r : int) -> str:
        """Overrides `Reducer.reduce()`"""
        return self.get_key((index+r+r) % self.size)
