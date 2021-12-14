import time
import string
from Reducer import Reducer

class ZeroOrderMarkov(Reducer):
    def __init__(self, string_len : int) -> None:
        """Overrides reducer.__init__()"""
        self.string_len = string_len
        self.alphabet = list(string.ascii_lowercase)
        self.mu = {'a': -247, 'b': -388, 'c': -309, 'd': -339, 'e': -219, 'f': -401, 'g': -370, 'h': -351, 'i': -258, 'j': -623, 'k': -451, 'l': -290, 'm': -350, 'n': -271, 'o': -264, 'p': -345, 'q': -623, 'r': -258, 's': -286, 't': -267, 'u': -332, 'v': -460, 'w': -435, 'x': -584, 'y': -403, 'z': -591}
        self.threshold = self.mu['a'] * (self.string_len-2) + self.mu['o'] + self.mu['w']
        self.threshold = -1590
        self.partial_size = {x:{} for x in range(0,self.string_len+1)}
        self.size = self.__build_dictionary()

    def __partial_size1(self, current_length, level) -> int:
        """The size of the remaining keyspace at current_length and level"""
        if level < self.threshold:
            self.partial_size[current_length][level] = 0
            return 0
        if self.string_len == current_length:
            self.partial_size[current_length][level] = 1
            return 1

        sum = 0
        for char in self.alphabet:
            new_length = current_length+1
            new_level = level+self.mu[char]
            if new_level in self.partial_size[new_length]:
                sum += self.partial_size[new_length][new_level]
            else:
                sum += self.__partial_size1(new_length,new_level)
        self.partial_size[current_length][level] = sum

        return sum

    def __build_dictionary(self) -> int:
        """Builds a dictionary according to given params

        Returns:
            int: The size of the keyspace
        """
        return self.__partial_size1(0,0)

    def __get_key1(self, current_length : int, i : int, level : int) -> str:
        """Helper function for get_key"""
        if self.string_len == current_length:
            return ""

        sum = 0
        for char in self.alphabet:
            new_level = level+self.mu[char]
            size = self.partial_size[current_length+1][new_level]
            if sum+size > i:
                return char + self.__get_key1(current_length+1, i-sum, new_level)
            sum = sum+size
        raise("index larger than keyspace size")

    def get_key(self, i : int) -> str:
        """Gets the i-th key in our Markov dictionary

        Args:
            index (int): Index of key in our Markov dictionary

        Returns:
            str: The i-th key in our Markov Dictionary
        """
        return self.__get_key1(0,i,0)

    def reduce(self, hash : int, r : int) -> str:
        """Overrides `Reducer.reduce()`"""
        return self.get_key((hash + r) % self.size)
