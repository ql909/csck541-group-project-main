# Documentation "server_test.py"
The server_test.py file contains the set of unit tests for the server.py module in the network. The tests use the unittest framework for writing and executing test cases. The purpose of these tests is to ensure that the functions in the server.py module behave as expected and produce the desired results.

## Test Cases
test_start_server(): This test case verifies the functionality of the start_server() function in the server module. It uses the patch function from the unittest.mock module to mock the behavior of the socket.socket function. The test simulates the server receiving a test data and checks if the expected actions occur, such as the printing of a connection message and sending the test data back.

test_serialised_receive_binary(): This test case tests the serialised_receive() function in the server module when handling binary data. It assigns a binary data string to the inc_data variable in the server module and checks if the function correctly prints the parsed data.

test_serialised_receive_json(): This test case tests the serialised_receive() function in the server module when handling JSON data. Similar to the previous test case, it assigns a JSON data string to the inc_data variable and checks if the function correctly prints the parsed data.

test_xml_deserialise(): This test case verifies the functionality of the xml_deserialise() function in the server module. It provides a sample XML message and checks if the function correctly deserializes it into a Python dictionary.

test_file_receive(): This test case tests the file_receive() function in the server module. It assigns a test file content string to the inc_data variable and checks if the function correctly prints the received file content.

test_file_receive_encrypted(): This test case tests the file_receive() function in the server module with encrypted test data. It assigns an encrypted test file content string to the inc_data variable and checks if the function correctly decrypts the data and prints the decrypted file content.

test_file_creator(): This test case verifies the functionality of the file_creator() function in the server module. It checks if the function correctly creates a file with the provided content and file prefix.

## Test Execution
The unittest.main() function at the end of the file ensures that the tests defined in the TestServer class are executed when the server_test.py script is run as the main script. It runs all the test cases and displays the test results, indicating whether each test case passed or failed.

# Documentation "client_test.py"
The client_test.py file contains a set of unit tests for the client.py module. These tests are written using the unittest framework and are designed to verify the behavior and functionality of various functions in the client.py module.

## Test Cases
test_user_input_valid_input(): This test case verifies the functionality of the user_input() function in the client module. It uses the patch function from the unittest.mock module to mock the behavior of the input function. The test checks if the function correctly returns the valid input provided by the user.

test_user_input_invalid_and_valid_input(): This test case tests the user_input() function with both invalid and valid inputs. It uses the side_effect parameter of the patch function to simulate multiple user inputs. The test checks if the function handles the invalid input and prompts the user to choose a correct option.

test_check_existing_file_valid_extension(): This test case verifies the functionality of the check_file() function in the client module when provided with an existing file and a valid extension. It uses the patch function to mock the behavior of the input function and checks if the function correctly identifies the existing file.

test_check_non_existent_file(): This test case tests the check_file() function when provided with a file that does not exist in the directory. It uses the file_exists function from the client module, patched to return False, and simulates user input for a non-existing file. The test checks if the function correctly raises a StopIteration exception and prints the appropriate error message.

test_check_existing_file_with_incorrect_extension(): This test case tests the check_file() function when provided with a file that exists in the directory but has an invalid file extension. It uses the file_exists function, patched to return True, and simulates user input for an existing file with an incorrect extension. The test checks if the function correctly raises a StopIteration exception and prints the appropriate error message.

test_check_file_empty_string(): This test case tests the check_file() function when provided with an empty string as input. It uses the file_exists function, patched to return False, and simulates user input for an empty string. The test checks if the function correctly raises a StopIteration exception and prints the appropriate error message.

test_send_data_valid_input(): This test case verifies the functionality of the send_data() function in the client module when provided with valid input. It uses the patch function to mock the behavior of the socket.socket function and checks if the function correctly establishes a socket connection, sends the data, receives the response, and returns the expected result.

test_send_data_invalid_argument(): This test case tests the send_data() function when provided with an invalid message. It uses the StringIO object to capture the output of sys.stdout and checks if the function raises a ValueError and prints the appropriate error message.

test_serialise_binary_data(): This test case verifies the functionality of the serialise() function in the client module when serializing binary data. It checks if the function correctly serializes the provided dictionary into binary data and returns the expected result.

test_serialise_json_data(): This test case tests the serialise() function when serializing JSON data. It checks if the function correctly serializes the provided dictionary into JSON data and returns the expected result.

test_serialise_xml_with_valid_data(): This test case tests the serialise() function when serializing XML data. It checks if the function correctly serializes the provided dictionary into XML data and returns the expected result.

test_serialise_invalid_serialisation_type(): This test case tests the serialise() function when provided with an invalid serialization type. It checks if the function raises a ValueError as expected.

test_parse_final_data(): This test case verifies the functionality of the parse_final_data() function in the client module. It checks if the function correctly concatenates the provided data and options into a final data string before sending it.

## Test Execution
The unittest.main() function at the end of the file ensures that the tests defined in the TestClient class are executed when the client_test.py script is run as the main script. It runs all the test cases and displays the test results, indicating whether each test case passed or failed.

# Documentation "utils_test.py"
The utils_test.py file contains utility functions for encryption and dictionary creation. These functions are designed to provide encryption and decryption capabilities using the Fernet encryption scheme from the cryptography library, as well as the creation of a custom dictionary.

## Encryption Utils
retrieve_key(): This function retrieves the encryption key from the key.key file. It reads the key from the file and returns it as bytes. If the key is not found or empty, it raises a ValueError indicating the absence of the encryption key.

decrypt(data): This function decrypts the given encrypted data using the Fernet encryption scheme. It takes the encrypted data as bytes and decrypts it using the encryption key retrieved from retrieve_key(). The decrypted data is returned as a string. If the data fails to decrypt, it raises a cryptography.fernet.InvalidToken exception.

encrypt(data): This function encrypts the given data using the Fernet encryption scheme. It takes the data as a string and encrypts it using the encryption key retrieved from retrieve_key(). The encrypted data is returned as bytes.

## Dictionary Creation
generate_dict(): This function allows the user to create a valid, custom dictionary. It prompts the user to enter the number of dictionary entries they would like to create and validates the input as an integer. Then, it iteratively prompts the user to enter a key and a value for each entry, ensuring that the key is a non-empty string. The function returns the user-generated dictionary as the result.

## Key Retrieval
The encryption key is retrieved using the retrieve_key() function, and the key is stored in the KEY variable for later use by the encryption and decryption functions.