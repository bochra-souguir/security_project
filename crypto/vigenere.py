
def encrypt(plaintext, key):
    """
        
    Exemple:
        >>> encrypt("HELLO", "KEY")
        'RIJVS'
    """
    if not key or not key.isalpha():
        raise ValueError("La clé doit contenir uniquement des lettres")
    
    key = key.upper()
    ciphertext = []
    key_index = 0
    
    for char in plaintext:
        if char.isupper():
            # Décalage selon la lettre de la clé
            shift = ord(key[key_index % len(key)]) - 65
            shifted = ((ord(char) - 65 + shift) % 26) + 65
            ciphertext.append(chr(shifted))
            key_index += 1
        elif char.islower():
            shift = ord(key[key_index % len(key)]) - 65
            shifted = ((ord(char) - 97 + shift) % 26) + 97
            ciphertext.append(chr(shifted))
            key_index += 1
        else:
            # Conserver non-alphabétiques sans avancer dans la clé
            ciphertext.append(char)
    
    return ''.join(ciphertext)


def decrypt(ciphertext, key):

    if not key or not key.isalpha():
        raise ValueError("La clé doit contenir uniquement des lettres")
    
    key = key.upper()
    plaintext = []
    key_index = 0
    
    for char in ciphertext:
        if char.isupper():
            shift = ord(key[key_index % len(key)]) - 65
            shifted = ((ord(char) - 65 - shift) % 26) + 65
            plaintext.append(chr(shifted))
            key_index += 1
        elif char.islower():
            shift = ord(key[key_index % len(key)]) - 65
            shifted = ((ord(char) - 97 - shift) % 26) + 97
            plaintext.append(chr(shifted))
            key_index += 1
        else:
            plaintext.append(char)
    
    return ''.join(plaintext)