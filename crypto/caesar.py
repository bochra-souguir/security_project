def encrypt(plaintext, key):
    """
    Chiffre un texte avec César
    """
    # Validation du type
    if not isinstance(key, int):
        raise ValueError("La clé doit être un entier")

    # On prend la clé modulo 26
    key = key % 26

    ciphertext = []
    for char in plaintext:
        if char.isupper():
            shifted = ((ord(char) - 65 + key) % 26) + 65
            ciphertext.append(chr(shifted))
        elif char.islower():
            shifted = ((ord(char) - 97 + key) % 26) + 97
            ciphertext.append(chr(shifted))
        else:
            ciphertext.append(char)
    return ''.join(ciphertext)


def decrypt(ciphertext, key):
    """
    Déchiffre un texte chiffré avec César
    """
    # Le déchiffrement est un chiffrement avec la clé opposée
    return encrypt(ciphertext, -key)


def bruteforce(ciphertext):
    """
    Génère tous les candidats possibles (25 clés)
    
    Args:
        ciphertext (str): Texte chiffré
    
    Returns:
        list: Liste de tuples (clé, plaintext)
    
    Exemple:
        >>> candidates = bruteforce("KHOOR")
        >>> len(candidates)
        25
    """
    candidates = []
    
    for key in range(1, 26):
        plaintext = decrypt(ciphertext, key)
        candidates.append((key, plaintext))
    
    return candidates