class Reducer:
    """A generic class that provides a reducer function"""

    def __init__(self, string_len):
        """Initializes a reducer for `string_len`

        Args:
            string_len (int): The length of the string a reducer should produce
        """
        pass

    def reduce(self,index,r):
        """A generic reducer function

        Args:
            hash (bool): a hash to reduce
            r (int): the reducer number to use

        Returns:
            string: the reduced hash
        """
        pass

    def get_key(self, i : int) -> str:
        pass