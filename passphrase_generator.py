import random
import socket
import math
from cryptography.fernet import Fernet

def load_words(filename="positive_words.txt"):
    with open(filename, "r") as file:
        return [word.strip() for word in file if word.strip()]

def generate_passphrase(word_count=4):
    words = load_words(f"{theme}_words.txt")
    return '-'.join(random.sample(words, word_count)), len(words)

def calculate_entropy(word_count, word_list_size):
    return word_count * math.log2(word_list_size)

def encrypt_passphrase(passphrase):
    key = Fernet.generate_key()  
    fernet = Fernet(key)        
    encrypted = fernet.encrypt(passphrase.encode())  
    return encrypted, key  

def send_passphrase(encrypted_pass, host="127.0.0.1", port=5000):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))          
            s.sendall(encrypted_pass)        
            print("Encrypted passphrase sent to the server!")
    except ConnectionRefusedError:
        print("Couldn't connect to the server. Is it running?")

if __name__ == "__main__":
    print("Welcome to the Passphrase Generator.")

    theme = input("Pick a theme (positive / networking / security): ").strip().lower()

    passphrase, list_size = generate_passphrase(theme=theme)

    print(f"\n Your brand new passphrase: {passphrase}")

    entropy = calculate_entropy(len(passphrase.split('-')), list_size)
    print(f" Estimated passphrase strength: {entropy:.2f} bits")

    
    encrypted, key = encrypt_passphrase(passphrase)
    print(f"\n🔒 Encrypted version (for sending safely):\n{encrypted.decode()}")
    print(f"🗝️  Secret key (needed to decrypt it later, so don’t lose it!):\n{key.decode()}")

   
    send_it = input("\n📡 Want to send it to a server? (y/n): ").strip().lower()
    if send_it == 'y':
        send_passphrase(encrypted)
    else:
        print("Your passphrase is safe and local.")
