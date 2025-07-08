import random

def load_words(filename="positive_words.txt"):
    with open(filename, "r") as file:
        return [word.strip() for word in file if word.strip()]

def generate_passphrase(word_count=4):
    words = load_words()
    return '-'.join(random.sample(words, word_count))

if __name__ == "__main__":
    print("Your positive passphrase is:")
    print(generate_passphrase())

