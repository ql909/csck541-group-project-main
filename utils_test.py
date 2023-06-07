import unittest
from unittest.mock import patch
from utils import retrieve_key, decrypt, encrypt, generate_dict

class UtilsTest(unittest.TestCase):
    """ This is a unit testing class for the utility encryption and dictionary 
    generation functions used by the network.
    """
    def test_retrieve_key(self):
        """Test that the retrieve_key function can successfully retrieve the
        encryption key from the config file.
        """
        with open("key.key", "rb") as key_file:
            key = key_file.read().strip()

        self.assertEqual(retrieve_key(), key)


    def test_decrypt(self):
        """Test that the decrypt function can successfully decrypt
        the given data using the Fernet encryption scheme.
        """
        encrypted_data = b'gAAAAABkaf_7fqY1iO6hXlda0LogqczXBVUNw-uhgq-3PlCK' \
                         b'CfA5JXrmbgE9Qinf0drsnbABvDS4LpQhRWNxRsMruMDX8LpM' \
                         b'-UwloaRFz0ZPZFBZ0eFhl-c='
        decrypted_data = decrypt(encrypted_data)

        self.assertEqual(decrypted_data, "This is some encrypted data.")


    def test_encrypt(self):
        """Test that the encrypt function can successfully encrypt 
        the given data using the Fernet encryption scheme.
        """

        data = "This is some data to be encrypted.".encode()
        encrypted_data = encrypt(data)

        self.assertNotEqual(encrypted_data, data)


    def test_generate_dict(self):
        """Test that the generate_dict function can successfully create 
        a custom dictionary.
        """

        with patch('builtins.input', side_effect=['1', 'key', 'value']):
            user_dict = generate_dict()

        self.assertGreater(len(user_dict), 0)
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['key'], 'value')

if __name__ == "__main__":
    unittest.main()
