import unittest
from unittest.mock import patch, MagicMock
import server


class TestServer(unittest.TestCase):
    """Unit testing class for the server.py module in the network"""

    def test_start_server(self):
        """
        Test case for the start_server() function in the server module.
        """
        with patch('socket.socket') as mock_socket:
            mock_conn = MagicMock()
            # simulate an empty response (None) to break the loop:
            mock_conn.recv.side_effect = [b'Test Data', None]
            mock_socket.return_value.__enter__ \
                                    .return_value.accept.return_value = (
                mock_conn, ('127.0.0.1', 1234))

            with patch('builtins.print') as mock_print:
                server.start_server()
                mock_print.assert_called_with('127.0.0.1 Connected')
                mock_conn.sendall.assert_called_with(b'Test Data')

    def test_serialised_receive_binary(self):
        """
        Test case for the serialised_receive() function in the server 
        module handling binary data.
        """
        # have to assign inc_data str with user options to parse
        server.inc_data = str(b'1~pickle~\\x80\\x04\\x95\\x12\\x00\\x00\\x0' \
                              b'0\\x00\\x00\\x00\\x00}\\x94\\x8c\\x03' \
                              b'key\\x94\\x8c\\x05value\\x94s.~1'
                             )
        
        with patch('builtins.print') as mock_print:
            server.serialised_receive()
            mock_print.assert_called_with("You provided the server with:\n" \
                                            "{'key': 'value'}"                                         
                                            )

    def test_serialised_receive_json(self):
        """
        Test case for the serialised_receive() function in the server 
        module handling JSON data.
        """
        # have to assign inc_data str with user options to parse
        server.inc_data = str(b'1~json~{\\n    "key": "value"\\n}~1')

        with patch('builtins.print') as mock_print:
            server.serialised_receive()
            mock_print.assert_called_with("You provided the server with:\n" \
                                              "{'key': 'value'}"                                         
                                             )


    def test_xml_deserialise(self):
        """
        Test case for the xml_deserialise() function in the server module.
        """
        message = b'<root><key>value</key></root>'

        result = server.xml_deserialise(message)
        self.assertEqual(result, {'key': 'value'})


    def test_file_receive(self):
        """
        Test case for the file_receive() function in the server module.
        """
        server.inc_data = str(b'n~Test File Content~1')

        with patch('builtins.print') as mock_print:
            server.file_receive()
            mock_print.assert_called_with(
                "\nYou provided the server with:\nTest File Content")


    def test_file_receive_encrypted(self):
        """
        Test case for the file_receive() function in the server module.
        with encrypted test data
        """
        # 'Test File Content' encrypted with Fernet
        server.inc_data = str(b'y~gAAAAABkafF1IixRZ8vdNSCWvMdjEbZHM9ZUp6NVV' \
                              b'EpEhbmskvqsFH_HF3CPR6P9fvPnqzwuwGTJsjworivI' \
                              b'Xvdr1wQQUo-cDBKi-svQEdbQ6TxUZppPk_w=~1')

        with patch('builtins.print') as mock_print:
            server.file_receive()
            mock_print.assert_called_with(
                "\nYour decrypted file contents:\nTest File Content")


    def test_file_creator(self):
        """
        Test case for the file_creator() function in the server module.
        """
        content = 'Test File Content'
        file_prefix = 'test_file'

        with patch('builtins.open') as mock_open:
            server.file_creator(content, file_prefix)
            mock_open.assert_called_with(
                'test_file1.txt', 'w', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()