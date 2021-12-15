from hashlib import md5

class Rainbow():
    def __init__(self, chains, rounds, reducer):
        self.table = {}
        self.max_chains = chains
        self.rounds = rounds
        self.reducer = reducer
        self.chains = self.build_table()

    def build_table(self):
        '''Build a rainbow table'''
        for chain_no in range(0,self.max_chains):
            init = self.reducer(chain_no,0)

            plaintext = init
            for round in range(0,self.rounds):
                ciphertext = md5(plaintext.encode('ascii')).hexdigest()
                plaintext=self.reducer(int(ciphertext,16), round)

            self.table[plaintext.encode('ascii')] = init
        return len(self.table)

    def collision_rate(self):
        '''Calculate the estimated collision rate'''
        return 1 - (self.chains/self.max_chains)

    def encoded_upper_bound(self):
        '''Calculates the approximate number of passwords our table encodes'''
        return self.chains * self.rounds

    def crack_hash(self,hash):
        '''Attempts to crack `hash`'''
        for i in range(0,self.rounds):
            hypothesis = self.rounds - 1 - i
            ciphertext = int(hash,16)
            for j in range(hypothesis, self.rounds):
                plaintext = self.reducer(ciphertext, j).encode('ascii')
                ciphertext = int(md5(plaintext).hexdigest(),16)

            if plaintext in self.table:
                test_plaintext = self.table[plaintext].encode('ascii')
                for j in range(0, hypothesis):
                    test_ciphertext = int(md5(test_plaintext).hexdigest(),16)
                    test_plaintext = self.reducer(test_ciphertext, j).encode('ascii')
                test_ciphertext = md5(test_plaintext).hexdigest()
                if hash == test_ciphertext:
                    return test_plaintext
        return False