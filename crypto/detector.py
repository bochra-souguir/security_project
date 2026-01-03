"""
Détection automatique du type de chiffrement
Basé sur l'indice de coïncidence (IC)
"""

from collections import Counter
import math


def calculate_ic(text):
    """
    Calcule l'indice de coïncidence d'un texte
    
    L'IC mesure la probabilité que deux lettres prises au hasard
    soient identiques. Pour un texte en anglais : IC ≈ 0.065-0.075
    Pour un texte aléatoire : IC ≈ 0.038
    
    Args:
        text (str): Texte à analyser
    
    Returns:
        float: Indice de coïncidence (0-1)
    
    Formule:
        IC = Σ ni(ni-1) / N(N-1)
        où ni = fréquence de la lettre i
            N = nombre total de lettres
    """
    # Nettoyer : garder uniquement les lettres
    text_clean = ''.join(c.upper() for c in text if c.isalpha())
    n = len(text_clean)
    
    if n < 2:
        return 0.0
    
    # Compter les fréquences
    freq = Counter(text_clean)
    
    # Calculer IC
    ic = sum(count * (count - 1) for count in freq.values())
    ic /= (n * (n - 1))
    
    return ic


def detect_cipher_type(ciphertext):
    """
    Détecte automatiquement le type de chiffrement
    
    Stratégie:
    - César : L'IC reste proche de celui du texte clair (≈ 0.065)
    - Vigenère : L'IC diminue (≈ 0.038-0.050)
    
    Args:
        ciphertext (str): Texte chiffré
    
    Returns:
        str: 'caesar' ou 'vigenere'
    
    Exemple:
        >>> detect_cipher_type("KHOOR ZRUOG")
        'caesar'
        >>> detect_cipher_type("RIJVS AMBPX")
        'vigenere'
    """
    ic = calculate_ic(ciphertext)
    
    # Seuil empirique (inspiré TP2)
    # IC > 0.055 → probablement César
    # IC ≤ 0.055 → probablement Vigenère
    
    threshold = 0.055
    
    if ic > threshold:
        return 'caesar'
    else:
        return 'vigenere'


def analyze_text_properties(text):
    """
    Analyse les propriétés statistiques d'un texte
    (utile pour le debugging)
    
    Args:
        text (str): Texte à analyser
    
    Returns:
        dict: Propriétés statistiques
    """
    text_clean = ''.join(c.upper() for c in text if c.isalpha())
    
    if not text_clean:
        return {
            'length': 0,
            'ic': 0.0,
            'entropy': 0.0,
            'most_common': []
        }
    
    freq = Counter(text_clean)
    n = len(text_clean)
    
    # Entropie de Shannon
    entropy = -sum((count/n) * math.log2(count/n) 
                   for count in freq.values())
    
    return {
        'length': n,
        'ic': calculate_ic(text),
        'entropy': entropy,
        'most_common': freq.most_common(5)
    }