"""Client Side

Run this file to send a dictionary
or send a text file to the server.
"""

import socket
import pickle
import json
from dict2xml import dict2xml
from utils import encrypt, generate_dict
from os.path import exists as file_exists 

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000

d_type=''

def user_input(prompt, choices):
    """Validate User Input
    Take user input and make sure
    it matches what the program is
    expecting

    Arguments:
    prompt -- Prompt message to display
    choices -- List of valid choices
    """
    while True:
        user_choice = input(f"\n{prompt}: ").lower()
        if user_choice in choices:
            return user_choice
        print("### Please choose a correct option ###")

def check_file():
    """Check if file exists and the file type is correct"""
    while True:
        path = input()
        file_extension = path.split(".")[-1]
        if file_exists(path):
            if file_extension == "txt":
                print("### File found ###")
                return path
            print("### Filetype is incorrect ###")
        else:
            print("### File does not exist ###")
        print("### Please enter your filename ending in .txt ###")

def send_data(serialised_data):
    """Send the data to the server"""
    if not isinstance(serialised_data, str):
        raise ValueError("Invalid data type. Provide a serialised string")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(serialised_data.encode('latin1'))
        data = s.recv(1024)
        return "Data Sent"

def serialise(user_dict, s_type):
    """Serialise data"""
    serialised = ""
    method = ""
    if s_type == '1':
        serialised = pickle.dumps(user_dict)
        method = "pickle"
    elif s_type == '2':
        serialised = json.dumps(user_dict, sort_keys=True, indent=4).encode()
        method = "json"
    elif s_type == '3':
        serialised = dict2xml(user_dict, wrap='root', indent="").encode()
        method = "xml"
    else:
        raise ValueError(f"Invalid serialisation method: {s_type}." \
                          " Please choose 1 (binary), 2 (JSON) or 3 (XML)")
                          
    return serialised, method

def parse_final_data(d_type, method, serialised, option):
    """Concatenate Optional Variables"""
    return f"{d_type}~{method}~{str(serialised)[2:-1]}~{option}"

def main():
    """Client Main Function"""
    print("\n" + "#" * 47)
    print(" Welcome to the Group C client/server network!\n" + "#" * 47)
    print("\nPlease choose from the following options: (type 1 or 2)",
          "\n(1) Create a dictionary and send it to the server.",
          "\n(2) Send a text file to the server.")
    choices = ["1", "2"]
    d_type = user_input("Option", choices)

    if d_type == "1":
        user_dict = generate_dict()
        print("\nPlease Choose Serialisation Type: (type 1, 2 or 3)",
              "\n(1) Binary\n(2) JSON\n(3) XML")
        choices = ["1", "2", "3"]
        s_type = user_input("Serialisation Type", choices)

        print("\nWhere would you like to output the data: (type 1 or 2)",
              "\n(1) On screen",
              "\n(2) Export to file")
        choices = ["1", "2"]
        option = user_input("Output Option", choices)

        serialised, method = serialise(user_dict, s_type)
        final_data = parse_final_data(d_type, method, serialised, option)

        if option == "2":
            print("\nDo you wish to locally encrypt your file? (Y) (N)")
            choices = ["y", "n"]
            enc_file_choice = user_input("Encryption Choice", choices)

            file_contents = str(user_dict)

            if enc_file_choice == "y":
                enc_file_content = encrypt(file_contents.encode())
                enc_file_name = input("\nPlease enter a name for your text file: ")
                if not enc_file_name.endswith(".txt"):
                    enc_file_name += ".txt"

                with open(enc_file_name, 'wb') as file:
                    file.write(enc_file_content)

                print(f"{enc_file_name} created!")
                final_data = enc_file_content.decode()

        send_data(final_data)
        print("\n### Your data has been sent ###")

    else:
        print("\n### File Section ###")
        print("\n### Please enter your filename ending in .txt ###")

        file_choice = check_file()

        with open(file_choice, "r", encoding="utf-8") as file:
            file_contents = "".join(file.readlines())

        print("\nIs your file encrypted? (Y) (N)")
        choices = ["y", "n"]
        is_encrypted = user_input("Encryption Choice", choices)

        print("\nWhere would you like to output the data: (type 1 or 2)",
              "\n(1) On screen",
              "\n(2) Export to file")
        choices = ["1", "2"]
        option = user_input("Output Option", choices)

        final_data = f"{is_encrypted}~{file_contents}~{option}"

        if option == "2":
            print("\nDo you wish to locally encrypt your file? (Y) (N)")
            choices = ["y", "n"]
            enc_file_choice = user_input("Encryption Choice", choices)

            if enc_file_choice == "y":
                enc_file_content = encrypt(file_contents.encode())
                file_choice = file_choice.replace("/", "\\")
                file_choice = file_choice.split("\\")
                file_choice = file_choice[-1]
                split_name = file_choice.rsplit(".", 1)
                enc_file_name = split_name[0] + "_enc.txt"

                with open(enc_file_name, 'w', encoding="utf-8") as file:
                    file.write(enc_file_content.decode())

                print(f"{enc_file_name} created!")
                final_data = enc_file_content.decode()

        send_data(final_data)
        print("\n### Your data has been sent ###")

if __name__ == "__main__":
    main()
