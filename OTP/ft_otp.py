import sys
import argparse
import time
import hmac
import hashlib
import getpass
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
# pyinstaller --onefile --hidden-import="Crypto.Cipher" --hidden-import="Crypto.Protocol" --hidden-import="Crypto.Random" ft_otp.py


def generate_totp(hex_key: str, time_step: int = 30, digits: int = 6) -> str:
    key = bytes.fromhex(hex_key)

    current_time = int(time.time())
    counter = current_time // time_step
    counter_bytes = counter.to_bytes(8, 'big')

    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    offset = hmac_hash[-1] & 0x0F
    four_bytes = hmac_hash[offset : offset + 4]
    large_int = int.from_bytes(four_bytes, 'big') & 0x7FFFFFFF

    modulo = 10 ** digits
    otp = large_int % modulo

    return str(otp).zfill(digits)


def encrypt_and_store_key(hex_key_path: str):
    try:
        with open(hex_key_path, "r") as f:
            hex_key = f.read().strip()
    except FileNotFoundError:
        sys.exit(f"Error: Key file not found at {hex_key_path}")

    if len(hex_key) < 64:
        sys.exit("Error: Key must be at least 64 hexadecimal characters.")
    try:
        bytes.fromhex(hex_key)
    except ValueError:
        sys.exit("Error: Key contains non-hexadecimal characters.")

    master_password = getpass.getpass("Enter a master password to encrypt the key: ")
    if not master_password:
        sys.exit("Error: Master password cannot be empty.")
    master_password_confirm = getpass.getpass("Confirm master password: ")
    if master_password != master_password_confirm:
        sys.exit("Error: Passwords do not match.")

    salt = get_random_bytes(16)
    encryption_key = scrypt(master_password, salt, 32, N=2**14, r=8, p=1)
    cipher = AES.new(encryption_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(hex_key.encode('utf-8'))

    with open("ft_otp.key", "wb") as f:
        f.write(salt)
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)
    
    print("Key was successfully encrypted and saved in ft_otp.key.")


def decrypt_and_read_key(encrypted_key_path: str) -> str:
    try:
        with open(encrypted_key_path, "rb") as f:
            salt = f.read(16)
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()
    except FileNotFoundError:
        sys.exit(f"Error: Encrypted key file not found at {encrypted_key_path}")

    master_password = getpass.getpass("Enter master password to decrypt key: ")
    encryption_key = scrypt(master_password, salt, 32, N=2**14, r=8, p=1)
    cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=nonce)

    try:
        decrypted_hex_key = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_hex_key.decode('utf-8')
    except (ValueError, KeyError):
        sys.exit("Error: Decryption failed. The master password may be incorrect or the file is corrupted.")


def main():
    parser = argparse.ArgumentParser(
        description="ft_otp: A program to manage and generate One-Time Passwords.",
        epilog="Example usage: ./ft_otp.py -g key.hex"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", dest="g_path", help="Generate and store an encrypted key from a file.")
    group.add_argument("-k", dest="k_path", help="Generate a new password from an encrypted key file.")

    args = parser.parse_args()

    if args.g_path:
        encrypt_and_store_key(args.g_path)
    elif args.k_path:
        try:
            decrypted_key = decrypt_and_read_key(args.k_path)
            otp_code = generate_totp(decrypted_key)
            print(f"Generated OTP: {otp_code}")
        except Exception as e:
            sys.exit(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()