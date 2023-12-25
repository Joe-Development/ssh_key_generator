import paramiko
from termcolor import colored
import getpass
import logging

def generate_ssh_keypair(key_type='rsa', key_size=2048, output_filename='my_key'):
    key = None

    if key_type not in ['rsa', 'dsa', 'ecdsa', 'ed25519']:
        print(colored("Invalid key type. Please choose from: rsa, dsa, ecdsa, ed25519", 'red'))
        return

    try:
        passphrase = getpass.getpass(colored("> Enter passphrase for private key (leave blank for no passphrase): ", 'cyan'))

        if not isinstance(key_size, int) or key_size <= 0:
            raise ValueError("Key size must be a positive integer")

        key = paramiko.RSAKey.generate(key_size)
        key.write_private_key_file(output_filename)

        separate_public_key = input(colored("> Do you want to generate a separate public key file? (yes/no, default is no): ", 'cyan')).lower()

        if separate_public_key == 'yes':
            with open(f'{output_filename}.pub', 'w') as public_key_file:
                public_key_file.write(f'{key.get_name()} {key.get_base64()}')
            print(colored(f"> Separate public key file '{output_filename}.pub' generated successfully", 'green'))

        print(colored("> SSH key pair generated successfully", 'green'))

        if passphrase:
            key.write_private_key_file(output_filename, password=passphrase)
            print(colored("> Private key encrypted successfully", 'green'))

    except ValueError as ve:
        logging.error(f"[ERROR]: {ve}")
        print(colored(f"[ERROR]: {ve}", 'red'))
    except Exception as e:
        logging.error(f"[ERROR]: Generating SSH key pair: {e}")
        print(colored(f"[ERROR]: Generating SSH key pair: {e}", 'red'))

if __name__ == "__main__":
    key_type = input(colored("> Enter key type (rsa, dsa, ecdsa, ed25519): ", 'cyan')).lower()
    
    while True:
        try:
            key_size = int(input(colored("> Enter key size (default is 2048): ", 'cyan')) or 2048)
            break
        except ValueError:
            print(colored("[ERROR]: Key size must be a valid integer", 'red'))

    output_filename = input(colored("> Enter output filename (default is 'my_key'): ", 'cyan')) or 'my_key'
    generate_ssh_keypair(key_type=key_type, key_size=key_size, output_filename=output_filename)
