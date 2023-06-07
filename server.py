#!/usr/bin/env python3
""" Server Side
Run this file to open the server.
"""

import socket
import pickle
import json
import sys
import xmltodict
import logging

from dict2xml import dict2xml
from utils import decrypt
from os.path import exists as file_exists

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO)

# Data from socket
inc_data = ""

def start_server():
    """
    Starts the server and listens for incoming connections.
    """
    global inc_data

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            logging.info("Server bound to %s:%s", HOST, PORT) 
        except socket.error as binding_error:
            logging.error("Unable to bind to %s:%s", HOST, PORT)
            raise binding_error
        
        print(f"Server Open on {HOST}:{PORT}")
        s.listen()
        #s.settimeout(100)
        
        conn, addr = s.accept()
        with conn:
            logging.info("%s Connected", addr[0])
            print(f"{addr[0]} Connected")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                inc_data = repr(data)
                logging.info("Received data: %s", inc_data)


def serialised_receive():
    """Receiving Serialised data"""

    # Parse out serialisation and output methods (accepts '~'s in data too)
    parsed_methods = inc_data[2:-1].split('~',2)
    serialisation_method = parsed_methods[1]
    output_method = parsed_methods[-1].rsplit('~',1)[1]

    # Parse received data
    message = parsed_methods[-1].rsplit('~',1)[0].replace('\\\\', '\\')
    message = message.encode('utf-8')
    message = message.decode('unicode-escape').encode('latin1')

    # De-serialise data
    deserial_functions = {"pickle": pickle.loads,
                          "json": json.loads,
                          "xml": xml_deserialise
                         }

    dict_ = deserial_functions.get(serialisation_method)(message)


    # Output to screen or save to file
    if (output_method == "1"):
        print(f"You provided the server with:\n{dict_}")

    if (output_method == "2"):
        file_creator(str(dict_), "dictionary")


def xml_deserialise(message):
    """De-Serialise a Serialised XML string

    Keyword arguments:
    message -- the string to de-serialise
    """
    msg_parsed = str(message)[2:-1]
    msg_deserial = xmltodict.parse(msg_parsed)
    s_dict = msg_deserial["root"]
    try:
        s_dict.pop('#text')
        msg_dict = dict(s_dict)

        return(msg_dict)
    except KeyError:
        return(s_dict)


def file_receive():
    """Receiving File"""

    data_received = inc_data[4:-1]

    # Handle encrypted files
    if inc_data[2]=='y':
        # Decrypt and parse
        parse_encrypted = data_received.rsplit("~",1)
        decrypt_text = decrypt(parse_encrypted[0].encode())

        # Print if On screen selected
        if(parse_encrypted[-1] == "1"):
            print(f"\nYour decrypted file contents:\n{decrypt_text}")
        
        # Output to file otherwise
        if(parse_encrypted[-1] == "2"):
            file_creator(decrypt_text, "file")

    # Handle non-encrypted files
    if inc_data[2] == 'n':
        parsed_data = data_received.rsplit("~",1)
        
        # Print if On screen selected
        if(parsed_data[-1] == "1"):
            data_received = parsed_data[0]
            print(f"\nYou provided the server with:\n{data_received}")

        # Output to file otherwise
        if(data_received[-1] == "2"):
            data_received = parsed_data[0]
            content = ''.join(data_received)
            file_creator(content, "file")


def file_creator(content, file_prefix):
    """Create file

    Keyword arguments:
    content: Content of the file as a string.
    file prefix: The prefix to be used as the file name.
    """

    file_num = 1
    while True:
        filename = f"{file_prefix}{file_num}.txt"
        
        # Check if the file already exists in the current directory
        if not file_exists(filename):
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"{filename} created!")
            return True

        file_num += 1


def main():
    """ Server Main Function
    The starting point for execution for the programme.
    """
    global inc_data
    
    # Data from socket
    inc_data = ""

    # For testing serialised_receive()
    print("argv",sys.argv)
    if len(sys.argv) > 1:
        if(sys.argv[1] == "-T"):
            for _ in range(2):
                serialised_receive()
    else:
        start_server()
        if inc_data[2]=='1':
            serialised_receive()
        else:
            file_receive()


if __name__ == "__main__":
    main()
