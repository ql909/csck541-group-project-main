import unittest
from unittest.mock import patch
from io import StringIO
import client

class TestClient(unittest.TestCase):
    """Unit tests for the client module"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_input_valid_input(self):
        """Test user_input function with valid input"""

        with patch('builtins.input', return_value='1'):
            choice = client.user_input("Prompt", ["1", "2"])
            self.assertEqual(choice, "1")


    def test_user_input_invalid_and_valid_input(self):
        """Test user_input function with invalid followed by valid input"""

        with patch('builtins.input', side_effect=['3', '2']):
            with patch('sys.stdout', new=StringIO()) as invalid:
                choice = client.user_input("Prompt", ["1", "2"])
                self.assertEqual(choice, "2")
                expected_output = "### Please choose a correct option ###\n"
                self.assertEqual(invalid.getvalue(), expected_output)


    def test_check_existing_file_valid_extension(self):
        """Test check_file function with an existing file and valid
        extension
        """

        with patch('builtins.input', return_value='requirements.txt'):
            with patch('sys.stdout', new=StringIO()) as valid:
                file_path = client.check_file()
                self.assertEqual(file_path, 'requirements.txt')
                expected_output = "### File found ###\n"
                self.assertEqual(valid.getvalue(), expected_output)


    def test_check_non_existent_file(self):
        """Test check_file function with a file not in the directory"""

        with patch('client.file_exists', return_value=False):
            with patch('builtins.input', side_effect=['abcd.txt']):
                with patch('sys.stdout', new=StringIO()) as dummy:
                    with self.assertRaises(StopIteration):
                        file_path = client.check_file()
                        self.assertIsNone(file_path)
                        expected_output = "### File does not exist ###\n" \
                                          "### Please enter your filename" \
                                          "ending in .txt ###\n"
                        self.assertEqual(dummy.getvalue(), expected_output)


    def test_check_existing_file_with_incorrect_extension(self):
        """Test check_file function with a file in the directory that has an
           invalid file extension
        """
        with patch('client.file_exists', return_value=True):
            with patch('builtins.input', side_effect=['client.py']):
                with patch('sys.stdout', new=StringIO()) as dummy:
                    with self.assertRaises(StopIteration):
                        client.check_file()
                        expected_output = "### Filetype is incorrect ###\n" \
                                          "### Please enter a valid file path" \
                                          "ending in .txt ###\n"
                        self.assertEqual(dummy.getvalue(), expected_output)


    def test_check_file_empty_string(self):
        """Test check_file function with an empty string"""

        with patch('client.file_exists', return_value=False):
            with patch('builtins.input', side_effect=['']):
                with patch('sys.stdout', new=StringIO()) as dummy:
                    with self.assertRaises(StopIteration):
                        file_path = client.check_file()
                        self.assertIsNone(file_path)
                        expected_output = "### File does not exist ###\n" \
                                          "### Please enter your filename" \
                                          "ending in .txt ###\n"
                        self.assertEqual(dummy.getvalue(), expected_output)


    def test_send_data_valid_input(self):
        """test the send_data function with a typical input"""

        with patch('socket.socket') as mock_socket:
            mock_sendall = mock_socket.return_value \
                           .__enter__.return_value.sendall
            mock_recv = mock_socket.return_value.__enter__.return_value.recv
            mock_recv.return_value = b"Data Received"

            result = client.send_data("serialised_data")

            # Make sure the socket connection is good
            mock_socket.assert_called_once_with(
                client.socket.AF_INET, client.socket.SOCK_STREAM)
            mock_socket.return_value.__enter__ \
                                    .return_value \
                                    .connect.assert_called_once_with(
                                        (client.HOST, client.PORT)
                                    )

            # check data transfer and reception
            mock_sendall.assert_called_once_with(
                "serialised_data".encode('latin1'))
            mock_recv.assert_called_once_with(1024)

            # and make sure the return statement is working & printout is good
            self.assertEqual(result, "Data Sent")


    def test_send_data_invalid_argument(self):
        """test the send_data function with an invalid message"""

        with patch('sys.stdout', new=StringIO()) as invalid:
            with self.assertRaises(ValueError):
                client.send_data(123)

                expected_output = "Invalid data type. " \
                                  "Provide a serialized string ###\n"
                self.assertEqual(invalid.getvalue(), expected_output)


    def test_serialise_binary_data(self):
        """test binary serialisation"""

        expected_result = (b'\x80\x04\x95\x12\x00\x00\x00\x00\x00\x00\x00}' \
                           b'\x94\x8c\x03key\x94\x8c\x05value\x94s.',
                           'pickle'
                          )       
        user_dict = {"key": "value"}
        self.assertEqual(client.serialise(user_dict, '1'), expected_result)


    def test_serialise_json_data(self):
        """test JSON serialisation"""

        expected_result = (b'{\n    "key": "value"\n}', 'json')
        user_dict = {"key": "value"}
        self.assertEqual(client.serialise(user_dict, '2'), expected_result)


    def test_serialise_xml_with_valid_data(self):
        """test XML serialisation"""
        expected_result = (b'<root>\n<key>value</key>\n</root>', 'xml')

        user_dict = {"key": "value"}
        self.assertEqual(client.serialise(user_dict, '3'), expected_result)


    def test_serialise_invalid_serialisation_type(self):
        """test invalid serialisation type"""

        with self.assertRaises(ValueError):
            user_dict = {"key": "value"}
            client.serialise(user_dict, '4')


    def test_parse_final_data(self):
        """test parse_final_data_function to ensure everything is correctly 
        concatenated before sending the data
        """
        expected_result = r"1~pickle~\x80\x04\x95\x12\x00\x00\x00\x00\x00\x00\x" \
                            r"00}\x94\x8c\x03key\x94\x8c\x05value\x94s.~1"
        d_type = "1"
        method = "pickle"
        serialised = b'\x80\x04\x95\x12\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x03' \
                        b'key\x94\x8c\x05value\x94s.'
        option = "1"
        self.assertEqual(client.parse_final_data(d_type,
                                                    method,
                                                    serialised,
                                                    option),
                        expected_result
                        )


if __name__ == '__main__':
    unittest.main()
