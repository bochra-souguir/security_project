

def encrypt(plaintext, key):
    """
    Chiffre un texte avec César
    
    Args:
        plaintext (str): Texte en clair
        key (int): Clé de décalage (1-25)
    
    Returns:
        str: Texte chiffré
    
    Exemple:
        >>> encrypt("HELLO", 3)
        'KHOOR'
    """
    if not isinstance(key, int) or key < 1 or key > 25:
        raise ValueError("La clé doit être un entier entre 1 et 25")
    
    ciphertext = []
    
    for char in plaintext:
        if char.isupper():
            # Majuscules : A=65
            shifted = ((ord(char) - 65 + key) % 26) + 65
            ciphertext.append(chr(shifted))
        elif char.islower():
            # Minuscules : a=97
            shifted = ((ord(char) - 97 + key) % 26) + 97
            ciphertext.append(chr(shifted))
        else:
            # Conserver ponctuation, espaces, etc.
            ciphertext.append(char)
    
    return ''.join(ciphertext)


def decrypt(ciphertext, key):
    """
    Déchiffre un texte chiffré avec César
    
    Args:
        ciphertext (str): Texte chiffré
        key (int): Clé de décalage (1-25)
    
    Returns:
        str: Texte en clair
    
    Exemple:
        >>> decrypt("KHOOR", 3)
        'HELLO'
    """
    # Le déchiffrement est un chiffrement avec -key
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