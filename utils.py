from cryptography.fernet import Fernet

# Encryption Utils
def retrieve_key():
    """
    Retrieve the encryption key from the 'config' file.
    Returns: bytes: The encryption key.
    Raises: ValueError: If the encryption key is not found in the config file.
    """
    with open("key.key", "rb") as key_file:
        key = key_file.read().strip()
    if not key:
        raise ValueError("Encryption key not found.")
    return key

KEY = retrieve_key()

def decrypt(data):
    """
    Decrypt the given data using the Fernet encryption scheme.

    Args: data (bytes): The encrypted data.
    Returns: str: The decrypted data as a string.
    Raises: cryptography.fernet.InvalidToken: If the data fails to decrypt.
    """
    fernet_obj = Fernet(KEY)

    decrypted_data = fernet_obj.decrypt(data)
    return decrypted_data.decode()

def encrypt(data):
    """
    Encrypt the given data using the Fernet encryption scheme.
    
    Args: data (str): The data to be encrypted.
    Returns: bytes: The encrypted data.
    """
    fernet_obj = Fernet(KEY)
    encrypted_data = fernet_obj.encrypt(data)
    return encrypted_data

#Dictionary creation
def generate_dict():
    """Create a valid, custom dictionary
    
    Args: None
    Returns: dict: The user-generated dictionary
    """
    user_dict = {}

    while True:
        dictionary_length = input("\n### How many entries would you like? ###\n")
        try:
            dictionary_length = int(dictionary_length)
            break
        except ValueError:
            print("\n### Please enter a valid number ###")

    for v in range(dictionary_length):
        
        while True:
            dict_key = input(f"\n### Enter a key for entry {v} ###\nKey: ")
            
            if dict_key: break
            else: print("Key must be a non-empty string. Please try again.")

        dict_value = input(f"\n### Enter a value for entry {v} ###\nValue: ")
        user_dict[dict_key] = dict_value

    return user_dict
