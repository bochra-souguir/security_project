

from collections import Counter
from .vigenere import decrypt
from .scoring import score_text
import math


def find_repeated_sequences(text, min_length=3, max_length=5):
    """
    Trouve toutes les séquences répétées dans un texte
    
    Args:
        text (str): Texte à analyser
        min_length (int): Longueur minimale des séquences
        max_length (int): Longueur maximale des séquences
    
    Returns:
        dict: {séquence: [positions]}
    """
    text_clean = ''.join(c.upper() for c in text if c.isalpha())
    sequences = {}
    
    for seq_len in range(min_length, max_length + 1):
        for i in range(len(text_clean) - seq_len + 1):
            seq = text_clean[i:i + seq_len]
            
            if seq not in sequences:
                sequences[seq] = []
            
            sequences[seq].append(i)
    
    # Garder seulement les séquences répétées
    repeated = {seq: pos for seq, pos in sequences.items() 
                if len(pos) > 1}
    
    return repeated


def calculate_distances(positions):
    """
    Calcule les distances entre les positions répétées
    
    Args:
        positions (list): Liste de positions
    
    Returns:
        list: Liste de distances
    """
    distances = []
    for i in range(len(positions) - 1):
        dist = positions[i + 1] - positions[i]
        distances.append(dist)
    return distances


def get_factors(n):
    """
    Retourne tous les facteurs (diviseurs) d'un nombre
    
    Args:
        n (int): Nombre
    
    Returns:
        list: Liste de facteurs
    """
    factors = []
    for i in range(2, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors


def estimate_key_length(ciphertext, max_length=20):
    """
    Estime la longueur de la clé avec la méthode Kasiski
    
    Principe:
    1. Trouver les séquences répétées
    2. Calculer les distances entre répétitions
    3. Trouver le PGCD des distances
    
    Args:
        ciphertext (str): Texte chiffré
        max_length (int): Longueur maximale à tester
    
    Returns:
        int: Longueur estimée de la clé
    """
    # Trouver les séquences répétées
    repeated = find_repeated_sequences(ciphertext)
    
    if not repeated:
        # Fallback : essayer avec l'IC
        return estimate_key_length_ic(ciphertext, max_length)
    
    # Compter les facteurs de toutes les distances
    factor_counts = Counter()
    
    for seq, positions in repeated.items():
        distances = calculate_distances(positions)
        
        for dist in distances:
            factors = get_factors(dist)
            for f in factors:
                if f <= max_length:
                    factor_counts[f] += 1
    
    if not factor_counts:
        return estimate_key_length_ic(ciphertext, max_length)
    
    # Le facteur le plus commun est probablement la longueur
    most_common_factor = factor_counts.most_common(1)[0][0]
    
    return most_common_factor


def estimate_key_length_ic(ciphertext, max_length=20):
    """
    Estime la longueur de la clé avec l'indice de coïncidence
    
    Pour chaque longueur testée:
    1. Diviser le texte en sous-textes
    2. Calculer l'IC moyen
    3. La bonne longueur donne un IC proche de 0.065
    
    Args:
        ciphertext (str): Texte chiffré
        max_length (int): Longueur maximale à tester
    
    Returns:
        int: Longueur estimée de la clé
    """
    from .detector import calculate_ic
    
    text_clean = ''.join(c.upper() for c in ciphertext if c.isalpha())
    
    best_length = 1
    best_ic = 0
    
    for length in range(2, max_length + 1):
        # Diviser en sous-textes
        subtexts = [''] * length
        for i, char in enumerate(text_clean):
            subtexts[i % length] += char
        
        # Calculer IC moyen
        avg_ic = sum(calculate_ic(sub) for sub in subtexts) / length
        
        # Chercher l'IC le plus proche de 0.065 (anglais)
        if avg_ic > best_ic:
            best_ic = avg_ic
            best_length = length
    
    return best_length


def crack_vigenere_subtext(subtext):
    """
    Casse un sous-texte (chiffré comme César)
    
    Args:
        subtext (str): Sous-texte à analyser
    
    Returns:
        int: Clé la plus probable (0-25)
    """
    best_key = 0
    best_score = -1
    
    for key in range(26):
        # Déchiffrer comme César
        decoded = ''
        for char in subtext:
            if char.isupper():
                decoded += chr(((ord(char) - 65 - key) % 26) + 65)
            elif char.islower():
                decoded += chr(((ord(char) - 97 - key) % 26) + 97)
            else:
                decoded += char
        
        score = score_text(decoded)
        
        if score > best_score:
            best_score = score
            best_key = key
    
    return best_key


def crack_vigenere(ciphertext, top_n=5, data_dir='data'):
    """
    Casse automatiquement un chiffrement de Vigenère
    
    Stratégie:
    1. Estimer la longueur de la clé (Kasiski)
    2. Diviser en sous-textes
    3. Casser chaque sous-texte comme César
    4. Reconstruire la clé
    5. Déchiffrer et scorer
    
    Args:
        ciphertext (str): Texte chiffré
        top_n (int): Nombre de candidats à tester
        data_dir (str): Répertoire des données
    
    Returns:
        list: Liste de dictionnaires avec {key, score, plaintext}
    """
    print(f"[*] Analyse de Vigenère...")
    
    # Nettoyer le texte
    text_clean = ''.join(c.upper() for c in ciphertext if c.isalpha())
    
    # 1. Estimer la longueur de la clé
    key_length = estimate_key_length(ciphertext)
    print(f"[*] Longueur de clé estimée : {key_length}")
    
    # Tester aussi les longueurs voisines
    lengths_to_test = [key_length]
    if key_length > 1:
        lengths_to_test.append(key_length - 1)
    if key_length < 20:
        lengths_to_test.append(key_length + 1)
    
    candidates = []
    
    for length in lengths_to_test:
        # 2. Diviser en sous-textes
        subtexts = [''] * length
        for i, char in enumerate(text_clean):
            subtexts[i % length] += char
        
        # 3. Casser chaque sous-texte
        key_chars = []
        for subtext in subtexts:
            key_num = crack_vigenere_subtext(subtext)
            key_chars.append(chr(key_num + 65))
        
        key_str = ''.join(key_chars)
        
        # 4. Déchiffrer avec la clé trouvée
        plaintext = decrypt(ciphertext, key_str)
        score = score_text(plaintext, data_dir)
        
        candidates.append({
            'key': key_str,
            'key_length': length,
            'score': score,
            'plaintext': plaintext,
            'excerpt': plaintext[:150]
        })
        
        print(f"[*] Clé testée : {key_str} (longueur {length}) → score={score:.2f}")
    
    # Trier par score
    candidates.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"[✓] Meilleure clé : {candidates[0]['key']}, "
          f"score={candidates[0]['score']:.2f}") 
    return candidates[:top_n]

    def crack_vigenere_fast(ciphertext):
        """
        Version rapide : retourne uniquement le meilleur candidatArgs:
            ciphertext (str): Texte chiffréReturns:
            dict: Meilleur candidat
        """
        results = crack_vigenere(ciphertext, top_n=1)
        return results[0]
