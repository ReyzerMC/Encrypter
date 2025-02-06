import os
import hashlib
import base64
import json
from cryptography.fernet import Fernet
from getpass import getpass

ENCRYPTED_DIR = "encrypted"
KEY_FILE = "key.json"

def generate_key(password: str):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def save_key(key):
    with open(KEY_FILE, "w") as f:
        json.dump({"key": key.decode()}, f)

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            data = json.load(f)
            return data["key"].encode()
        
    return None

def encrypt_file(file_path, cipher):
    with open(file_path, "rb") as f:
        data = f.read()
    

    encrypt_data = cipher.encrypt(data)

    encrypt_path = os.path.join(ENCRYPTED_DIR, os.path.basename(file_path) + ".enc")
    with open(encrypt_path, "wb") as f:
        f.write(encrypt_data)
    

    os.remove(file_path)
    print(f"Archivo '{file_path}' encriptado con exito")


def decrypt_file(file_path, cipher):
    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    decrypted_path = file_path.replace(".enc", "")
    with open(decrypted_path, "wb") as f:
        f.write(decrypted_data)

    os.remove(file_path)
    print(f"Archivo '{decrypted_path}' descifrado con éxito.")

def main():
    if not os.path.exists(ENCRYPTED_DIR):
        os.makedirs(ENCRYPTED_DIR)
    
    if os.path.exists(KEY_FILE):
        password = getpass("Password: ")
        key = generate_key(password)

        if key.decode() != load_key().decode():
            print("Incorrect Password")
            return
    else:
        password = getpass("Establezca una contraseña para la encriptacion: ")
        key = generate_key(password)
        save_key(key)
    
    cipher = Fernet(key)

    while True:
        print("\n[1] Encriptar archivo\n[2] Desencriptar archivo\n[3] Salir")
        choice = input("Seleccione una opcion: ")

        if choice == "1":
            file_path = input("Ingrese la ruta")
            if os.path.exists(file_path):
                encrypt_file(file_path, cipher)
            else:
                print("Archivo no encontrado")
        
        elif choice == "2":
            file_path = input("Ingrese la ruta del archivo a desencriptar: ")
            if os.path.exists(file_path) and file_path.endswith(".enc"):
                decrypt_file(file_path, cipher)
            else:
                print("Archivo encriptado no encontrado o formato incorrecto.")
        
        elif choice == "3":
            print("Saliendo...")
            break

        else:
            print("Opcion Inválida.")
        
if __name__ == "__main__":
    main()