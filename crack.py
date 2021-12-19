import string
import time
import argparse

from Reducer import Reducer
from Rainbow import Rainbow
from ZeroOrderMarkov import ZeroOrderMarkov
from FirstOrderMarkov import FirstOrderMarkov
from random import randint

def create_dictionary(length : int, order : int = 0) -> Reducer:
    '''Creates a Markovian Dictionary and Returns the Reducer Object'''
    start = time.time()
    if order == 1:
        dictionary = FirstOrderMarkov(length)
    elif order == 0:
        dictionary = ZeroOrderMarkov(length)
    else:
        raise("Reducer Order Not Implemented")
    elapsed = time.time() - start
    print(f"Created an order {order} markov dictionary of size {dictionary.size} ({'{:.4f}'.format(dictionary.size*100/(26**length))}% of keyspace) [Time: {'{:.2f}'.format(elapsed)}s]")
    if(dictionary.size == 0):
        raise(Exception("Dictionary Size Zero"))
    return dictionary

def test_reducer_speed(dictionary : Reducer, test_size : int = 1000000) -> None:
    '''Tests the reducers speed at reducing `test_size` random values'''
    tests = [randint(0,10000000) for _ in range(test_size)]
    seconds = time.time()
    for key in tests:
        x = dictionary.reduce(key,0)
    elapsed = time.time()-seconds
    print("Elapsed:",elapsed)
    print("Per Keys:",elapsed/test_size)

def print_dictionary(dictionary : Reducer, max_keys : int = None, output_file : str = "dictionary.txt") -> None:
    max_keys = dictionary.size if not max_keys else min(max_keys, dictionary.size)
    with open(output_file, 'w') as f:
        for key in range(max_keys):
            print(dictionary.reduce(key, 0),file=f)

def test_on_file(test_file : str, rainbow_table : Rainbow, limit = 0) -> None:
    """A function to test the speed and success rate of a rainbow table

    Args:
        test_file (str): a string path to a text file consisting of password hashes and users
        rainbow_table (Rainbow): a Rainbow object to use for cracking `test_file`
    """
    tries = successes = 0
    start = time.time()
    with open(test_file,'r') as f, open("cracked.txt","w") as f2:
        for line in f:
            hash = line.strip().split(':')[0]
            plaintext = rainbow_table.crack_hash(hash)
            tries += 1
            if plaintext:
                successes += 1
                print(f"{hash}:{plaintext.decode()}", file=f2)
                print(f"{hash}:{plaintext.decode()} [Success Rate: {'{:.4f}'.format(successes*100/tries)}% ({successes}/{tries})]")
                if(limit > 0):
                    if successes == limit:
                        print(f"Cracked {successes} passwords in {time.time()-start} seconds with a {'{:.4f}'.format(successes*100/tries)}% success rate")
                        return
    print(f"Cracked {successes} passwords in {time.time()-start} seconds with a {'{:.4f}'.format(successes*100/tries)}% success rate")

def reduce_norm_gen(length : int):
    def reduce_norm(hash : int, r : int) -> str:
        """A non-probablistic reducer

        Args:
            hash (int): a hash to reduce
            r (int): the reducer number to use

        Returns:
            str: a 5-letter string
        """
        ret = ""
        for _ in range(length):
            ret += string.ascii_lowercase[(hash+r)%26]
            hash = hash//32
        return ret
    return reduce_norm

def main():
    parser = argparse.ArgumentParser(description='Break Hashes Using a Rainbow Table')
    either_group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--target-chains', '-c', dest='chains', type=int, required=True, help='the number of chains we should attempt to create')
    parser.add_argument('--chain-length', '-l', dest='length', type=int, required=True, help='the length each chain should have')
    parser.add_argument('--input-file', '-i', dest='file', default="data/6_letter_pw.txt", help='a file of password/hash combinations formatted \"{hash}:{password}\"')
    either_group.add_argument('--order', '-o', dest='order', default=0, type=int, choices=range(0,2), help='the order markov of the markov chain we should create')
    either_group.add_argument('--conventional', dest='conventional', action='store_true', help="Use a conventional reducer")
    parser.add_argument('--password-length', '-pl', dest='pwlen', default=6, type=int, help="The length of passwords we generate")
    parser.add_argument('--dry', dest='crack', action='store_false', help="Only show generation statistics")
    parser.add_argument('--limit', dest='limit', default=0, type=int, help="Maximimum passwords to crack")
    args = parser.parse_args()

    if args.conventional:
        rainbow_table = Rainbow(args.chains, args.length, reduce_norm_gen(args.pwlen))
    else:
        dictionary = create_dictionary(args.pwlen, args.order)
        rainbow_table = Rainbow(args.chains, args.length, dictionary.reduce)
    print("Collision Rate:",rainbow_table.collision_rate())
    encoded_upper_bound = rainbow_table.encoded_upper_bound()
    print("Encoded Passwords:",encoded_upper_bound,f"({'{:.4f}'.format(encoded_upper_bound*100/(26**args.pwlen))}% of keyspace)")
    if args.crack:
        test_on_file(args.file, rainbow_table, args.limit)

main()

